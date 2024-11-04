import re

def process_verilog_file(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Find the module block
    module_block = re.search(r'module\s+.*?endmodule', content, re.DOTALL)
    if not module_block:
        print("No module found in the file.")
        return

    module_content = module_block.group(0)

    # Extract output signal names with optional bit width
    bit_widths = re.findall(r'output\s+(\[\s*\d+:\s*\d+\s*\]\s*)?(\w+)', module_content)

    # Prepare the assign statements with bit width after the signal name
    assign_statements = "\n".join(
        [f"assign {signal}{width} = 0;" for width, signal in bit_widths]
    )

    # Insert assign statements before endmodule
    new_content = re.sub(r'(endmodule)', f"{assign_statements}\n\\1", module_content)

    # Replace the original module content with the new content
    final_content = content.replace(module_content, new_content)

    # Write to the new file
    with open(output_file, 'w') as file:
        file.write(final_content)

    print(f"Processed file saved as {output_file}")

if __name__ == '__main__':

    process_verilog_file('core.v', 'output.v')