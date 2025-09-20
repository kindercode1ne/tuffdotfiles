#!/usr/bin/python3
import sys
import os
import ipaddress
import fnmatch
from sys import stdout

def load_honeypot_patterns(honeypot_file):
    """Load honeypot IP patterns from file"""
    patterns = []
    
    try:
        with open(honeypot_file, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Extract IP pattern (remove comments after #)
                if '#' in line:
                    ip_pattern = line.split('#')[0].strip()
                else:
                    ip_pattern = line.strip()
                
                if ip_pattern:
                    patterns.append(ip_pattern)
    
    except FileNotFoundError:
        print(f"Error: Honeypot file '{honeypot_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading honeypot file: {e}")
        sys.exit(1)
    
    return patterns

def parse_bot_line(line):
    """Parse bot list line in format: IP:PORT USERNAME:PASSWORD"""
    try:
        line = line.strip()
        if not line or line.startswith('#'):
            return None
            
        # Split by space to separate IP:PORT from USERNAME:PASSWORD
        parts = line.split(' ', 1)
        if len(parts) != 2:
            return None
            
        ip_port = parts[0]
        user_pass = parts[1]
        
        # Parse IP:PORT
        if ':' not in ip_port:
            return None
        ip, port = ip_port.rsplit(':', 1)
        
        return {
            'ip': ip.strip(),
            'port': port.strip(),
            'credentials': user_pass.strip(),
            'full_line': line
        }
    except Exception:
        return None

def is_honeypot(ip, honeypot_patterns):
    """Check if IP matches any honeypot pattern"""
    try:
        # Convert IP to IPv4Address object for proper comparison
        ip_obj = ipaddress.IPv4Address(ip)
        
        for pattern in honeypot_patterns:
            # Handle different pattern types
            if pattern.endswith('*.*.*') or pattern.endswith('*.*') or pattern.endswith('*'):
                # Wildcard patterns like 192.168.*.* or 10.*.*.*
                if match_wildcard_pattern(ip, pattern):
                    return True, pattern
            elif '/' in pattern:
                # CIDR notation like 192.168.0.0/16
                try:
                    network = ipaddress.IPv4Network(pattern, strict=False)
                    if ip_obj in network:
                        return True, pattern
                except:
                    continue
            elif '-' in pattern:
                # Range notation like 192.168.1.1-192.168.1.254
                if match_range_pattern(ip, pattern):
                    return True, pattern
            else:
                # Exact IP match
                if ip == pattern:
                    return True, pattern
        
        return False, None
        
    except Exception:
        return False, None

def match_wildcard_pattern(ip, pattern):
    """Match IP against wildcard pattern like 192.168.*.*"""
    try:
        ip_parts = ip.split('.')
        pattern_parts = pattern.split('.')
        
        if len(ip_parts) != 4 or len(pattern_parts) != 4:
            return False
        
        for i in range(4):
            if pattern_parts[i] != '*' and ip_parts[i] != pattern_parts[i]:
                return False
        
        return True
    except:
        return False

def match_range_pattern(ip, pattern):
    """Match IP against range pattern like 62.0-30.*.*"""
    try:
        # Handle patterns like 62.0-30.*.*
        if '-' in pattern and '*' in pattern:
            pattern_parts = pattern.split('.')
            ip_parts = ip.split('.')
            
            if len(ip_parts) != 4 or len(pattern_parts) != 4:
                return False
            
            for i, part in enumerate(pattern_parts):
                if '*' in part:
                    continue
                elif '-' in part:
                    # Handle range in this octet
                    start, end = part.split('-')
                    try:
                        if not (int(start) <= int(ip_parts[i]) <= int(end)):
                            return False
                    except:
                        return False
                else:
                    # Exact match required
                    if ip_parts[i] != part:
                        return False
            
            return True
        
        return False
    except:
        return False

def main():
    if len(sys.argv) < 4:
        print("Usage: python " + sys.argv[0] + " <bot_list> <honeypot_list> <clean_output>")
        print("\nBot list format: IP:PORT USERNAME:PASSWORD")
        print("Example: 192.168.1.1:23 admin:password")
        print("\nThis script filters out honeypot IPs from your bot list")
        sys.exit()

    bot_file = sys.argv[1]
    honeypot_file = sys.argv[2]
    clean_output = sys.argv[3]
    
    # Load honeypot patterns
    print("Loading honeypot patterns...")
    honeypot_patterns = load_honeypot_patterns(honeypot_file)
    print(f"Loaded {len(honeypot_patterns)} honeypot patterns")
    
    # Stats
    total_bots = 0
    honeypot_count = 0
    clean_count = 0
    invalid_lines = 0
    
    print("\nChecking bot list against honeypots...")
    
    try:
        with open(bot_file, 'r') as f_in, open(clean_output, 'w') as f_out:
            for line_num, line in enumerate(f_in, 1):
                bot_data = parse_bot_line(line)
                
                if not bot_data:
                    invalid_lines += 1
                    continue
                
                total_bots += 1
                ip = bot_data['ip']
                
                # Check if IP is a honeypot
                is_hp, matched_pattern = is_honeypot(ip, honeypot_patterns)
                
                if is_hp:
                    honeypot_count += 1
                    print(f"\033[31m[HONEYPOT] {ip}:{bot_data['port']} -> Matches: {matched_pattern}\033[37m")
                else:
                    clean_count += 1
                    f_out.write(bot_data['full_line'] + '\n')
                    print(f"\033[32m[CLEAN] {ip}:{bot_data['port']}\033[37m")
                
                # Progress indicator
                if total_bots % 100 == 0:
                    stdout.write(f"\rProcessed {total_bots} bots...")
                    stdout.flush()
    
    except FileNotFoundError:
        print(f"Error: Bot file '{bot_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing files: {e}")
        sys.exit(1)
    
    # Final statistics
    print(f"\n\n=== HONEYPOT CHECK RESULTS ===")
    print(f"Total bots processed: {total_bots}")
    print(f"Clean bots: {clean_count}")
    print(f"Honeypots detected: {honeypot_count}")
    print(f"Invalid lines skipped: {invalid_lines}")
    
    if total_bots > 0:
        clean_percentage = (clean_count / total_bots) * 100
        honeypot_percentage = (honeypot_count / total_bots) * 100
        print(f"Clean rate: {clean_percentage:.2f}%")
        print(f"Honeypot rate: {honeypot_percentage:.2f}%")
    
    print(f"\nClean bot list saved to: {clean_output}")
    print("==============================")

if __name__ == "__main__":
    main()
