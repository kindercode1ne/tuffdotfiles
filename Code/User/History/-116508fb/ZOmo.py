#!/usr/bin/env python3

def clean_ip_port_file(input_file, output_file=None):
    """
    Read a file and keep only IP:port part from each line (remove everything after the first space)
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to the output file (optional, defaults to input_file with '_cleaned' suffix)
    """
    if output_file is None:
        # Create output filename by adding '_cleaned' before the extension
        if '.' in input_file:
            name, ext = input_file.rsplit('.', 1)
            output_file = f"{name}_cleaned.{ext}"
        else:
            output_file = f"{input_file}_cleaned"
    
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
        
        cleaned_lines = []
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Skip empty lines
                # Split by space and take only the first part (IP:port)
                ip_port = line.split(' ')[0]
                cleaned_lines.append(ip_port + '\n')
        
        with open(output_file, 'w') as outfile:
            outfile.writelines(cleaned_lines)
        
        print(f"Successfully processed {len(cleaned_lines)} lines")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    """
    Main function to run the IP:port cleaner
    """
    print("IP:Port File Cleaner")
    print("===================")
    
    # You can modify this to point to your specific file
    input_file = input("Enter the path to your input file: ").strip()
    
    # Optional: specify custom output file
    use_custom_output = input("Use custom output filename? (y/n): ").strip().lower()
    output_file = None
    
    if use_custom_output == 'y':
        output_file = input("Enter output filename: ").strip()
    
    clean_ip_port_file(input_file, output_file)

if __name__ == "__main__":
    main()