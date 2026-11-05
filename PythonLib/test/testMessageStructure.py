import DEFCOM._FlexibleMessageStructure as fms

def hexDump(buffer: bytes):
    """Prints the hex dump of a byte buffer."""
    print(' '.join([hex(i)[2:] for i in buffer]))

if __name__ == '__main__':
    print("Testing Message Structure")

    # Define structure using the order required by the C++ test
    # We create a list of tuples (key, type_string) to ensure order is preserved 
    # when constructing the dictionary.
    order_list = [
        ("myVarA", "int"),
        ("myVarB", "float"),
        ("myVarC", "double[3]"),
        ("myVarD", "long"),
        ("myVarE", "char[5]"),
        ("myVarF", "string[16]"),
        ("myVarG", "bytes[4]")
    ]
    
    # Convert list of tuples to an ordered dictionary
    inputDict = {key: type_str for key, type_str in order_list}

    # Construct the message structure
    print("\nMake Structure")
    ms = fms.MessageStructure(inputDict)
    print(f"Structure size is: {ms.totalSize}")

    # --- Test 1: Integer ---
    ms.setInt("myVarA", 10)
    print(f"\nint is: {ms.getInt('myVarA')} should be 10")
    print("Buffer after int:")
    hexDump(ms.getDecodeBuffer())

    # --- Test 2: Float ---
    ms.setFloat("myVarB", 123.45)
    print(f"\nfloat is: {ms.getFloat('myVarB')} should be 123.45")
    print("Buffer after float:")
    hexDump(ms.getDecodeBuffer())

    # --- Test 3: Double (Array access) ---
    ms.setDouble("myVarC", -123.456789, 2)
    # Note: This only sets the third double (index=2). The others remain uninitialized (0.0).
    print(f"\ndouble (index 2) is: {ms.getDouble('myVarC', 2)} should be -123.456789")
    print("Buffer after double:")
    hexDump(ms.getDecodeBuffer())

    # --- Test 4: Long ---
    ms.setLong("myVarD", 1234567890)
    print(f"\nlong is: {ms.getLong('myVarD')} should be 1234567890")
    print("Buffer after long:")
    hexDump(ms.getDecodeBuffer())

    # --- Test 5: Char (Single byte) ---
    # C++ 'a' is ASCII 97 (0x61)
    ms.setChar("myVarE", b'a')
    print(f"\nchar is: {ms.getChar('myVarE')} should be b'a'")
    print("Buffer after char:")
    hexDump(ms.getDecodeBuffer())

    # --- Test 6: String ---
    ms.setString("myVarF", "Hello World!")
    print(f"\nstring is: {ms.getString('myVarF')} should be Hello World!")
    print("Buffer after string:")
    hexDump(ms.getDecodeBuffer())

    # --- Test 7: Bytes ---
    bbytes_data = b'\x01\x02\x03\x04'
    ms.setBytes("myVarG", bbytes_data)
    
    # Read the bytes back using the getter (Python getter returns the data, it doesn't take a destination buffer)
    read_bytes = ms.getBytes("myVarG")
    print(f"\nbytes is: {read_bytes}")
    
    print("\n--- Final Buffer Dump ---")
    hexDump(ms.getDecodeBuffer())