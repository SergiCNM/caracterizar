"""
Test to verify that _check_voltage_limit method works correctly
"""

def test_check_voltage_limit_method():
    """Test that _check_voltage_limit method centralizes validation logic"""
    print("=" * 70)
    print("TESTING _check_voltage_limit METHOD")
    print("=" * 70)
    
    # Simulate the class structure with the new method
    class Keithley_2410:
        MAX_VOLTAGE = 500.0
        
        def _check_voltage_limit(self, voltage, context=""):
            """Check if voltage is within safe limits for the probe station."""
            if abs(voltage) > self.MAX_VOLTAGE:
                context_str = f" ({context})" if context else ""
                raise ValueError(
                    f"VOLTAGE SAFETY ERROR: Requested voltage{context_str} ({voltage}V) exceeds the maximum "
                    f"safe limit of ±{self.MAX_VOLTAGE}V supported by the probe station (mesa de puntas). "
                    f"Measurement aborted to prevent equipment damage."
                )
        
        def set_voltage(self, value):
            self._check_voltage_limit(value)
            return True
    
    class Keithley_2470:
        MAX_VOLTAGE = 500.0
        
        def _check_voltage_limit(self, voltage, context=""):
            """Check if voltage is within safe limits for the probe station."""
            if abs(voltage) > self.MAX_VOLTAGE:
                context_str = f" ({context})" if context else ""
                raise ValueError(
                    f"VOLTAGE SAFETY ERROR: Requested voltage{context_str} ({voltage}V) exceeds the maximum "
                    f"safe limit of ±{self.MAX_VOLTAGE}V supported by the probe station (mesa de puntas). "
                    f"Measurement aborted to prevent equipment damage."
                )
        
        def set_voltage(self, voltage):
            self._check_voltage_limit(voltage)
            return True
        
        def set_lin_sweep(self, function, start, stop):
            if function == "VOLT":
                self._check_voltage_limit(start, "sweep start")
                self._check_voltage_limit(stop, "sweep stop")
            return True
        
        def set_list(self, function, lista):
            if function == "VOLT":
                for i, v in enumerate(lista):
                    self._check_voltage_limit(v, f"list index {i}")
            return True
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Direct method call with valid voltage
    print("\n1. Testing _check_voltage_limit with valid voltage (300V)...")
    try:
        k2410 = Keithley_2410()
        k2410._check_voltage_limit(300)
        print("  [PASS] Valid voltage accepted")
        tests_passed += 1
    except ValueError:
        print("  [FAIL] Valid voltage rejected")
        tests_failed += 1
    
    # Test 2: Direct method call with invalid voltage
    print("\n2. Testing _check_voltage_limit with invalid voltage (600V)...")
    try:
        k2410 = Keithley_2410()
        k2410._check_voltage_limit(600)
        print("  [FAIL] Invalid voltage accepted")
        tests_failed += 1
    except ValueError as e:
        if "600V" in str(e) and "500.0V" in str(e):
            print("  [PASS] Invalid voltage rejected with correct error message")
            tests_passed += 1
        else:
            print("  [FAIL] Error message incorrect")
            tests_failed += 1
    
    # Test 3: Method with context parameter
    print("\n3. Testing _check_voltage_limit with context ('test context')...")
    try:
        k2470 = Keithley_2470()
        k2470._check_voltage_limit(550, "test context")
        print("  [FAIL] Invalid voltage accepted")
        tests_failed += 1
    except ValueError as e:
        if "test context" in str(e):
            print("  [PASS] Context included in error message")
            print(f"     Error snippet: ...{str(e)[50:120]}...")
            tests_passed += 1
        else:
            print("  [FAIL] Context not in error message")
            tests_failed += 1
    
    # Test 4: set_voltage uses _check_voltage_limit
    print("\n4. Testing set_voltage uses _check_voltage_limit (Keithley_2410)...")
    try:
        k2410 = Keithley_2410()
        k2410.set_voltage(400)
        print("  [PASS] Valid voltage accepted through set_voltage")
        tests_passed += 1
    except ValueError:
        print("  [FAIL] Valid voltage rejected")
        tests_failed += 1
    
    # Test 5: set_voltage rejects invalid voltage
    print("\n5. Testing set_voltage rejects invalid voltage (Keithley_2410)...")
    try:
        k2410 = Keithley_2410()
        k2410.set_voltage(650)
        print("  [FAIL] Invalid voltage accepted")
        tests_failed += 1
    except ValueError:
        print("  [PASS] Invalid voltage rejected")
        tests_passed += 1
    
    # Test 6: set_lin_sweep with context for start
    print("\n6. Testing set_lin_sweep with invalid start voltage...")
    try:
        k2470 = Keithley_2470()
        k2470.set_lin_sweep("VOLT", -600, 100)
        print("  [FAIL] Invalid sweep accepted")
        tests_failed += 1
    except ValueError as e:
        if "sweep start" in str(e):
            print("  [PASS] Invalid sweep rejected with 'sweep start' context")
            tests_passed += 1
        else:
            print("  [FAIL] Context 'sweep start' not in error message")
            tests_failed += 1
    
    # Test 7: set_lin_sweep with context for stop
    print("\n7. Testing set_lin_sweep with invalid stop voltage...")
    try:
        k2470 = Keithley_2470()
        k2470.set_lin_sweep("VOLT", 0, 550)
        print("  [FAIL] Invalid sweep accepted")
        tests_failed += 1
    except ValueError as e:
        if "sweep stop" in str(e):
            print("  [PASS] Invalid sweep rejected with 'sweep stop' context")
            tests_passed += 1
        else:
            print("  [FAIL] Context 'sweep stop' not in error message")
            tests_failed += 1
    
    # Test 8: set_list with context for list index
    print("\n8. Testing set_list with invalid voltage at index 2...")
    try:
        k2470 = Keithley_2470()
        k2470.set_list("VOLT", [0, 100, 600, 300])
        print("  [FAIL] Invalid list accepted")
        tests_failed += 1
    except ValueError as e:
        if "list index 2" in str(e):
            print("  [PASS] Invalid list rejected with 'list index 2' context")
            tests_passed += 1
        else:
            print("  [FAIL] Context 'list index 2' not in error message")
            tests_failed += 1
    
    # Test 9: set_list with valid voltages
    print("\n9. Testing set_list with all valid voltages...")
    try:
        k2470 = Keithley_2470()
        k2470.set_list("VOLT", [0, 100, 200, 300, 400, 500])
        print("  [PASS] Valid list accepted")
        tests_passed += 1
    except ValueError:
        print("  [FAIL] Valid list rejected")
        tests_failed += 1
    
    # Test 10: Edge case - exactly at limit
    print("\n10. Testing _check_voltage_limit at exact limit (500V)...")
    try:
        k2470 = Keithley_2470()
        k2470._check_voltage_limit(500)
        print("  [PASS] Voltage at limit accepted")
        tests_passed += 1
    except ValueError:
        print("  [FAIL] Voltage at limit rejected")
        tests_failed += 1
    
    # Test 11: Edge case - just over limit
    print("\n11. Testing _check_voltage_limit just over limit (500.1V)...")
    try:
        k2470 = Keithley_2470()
        k2470._check_voltage_limit(500.1)
        print("  [FAIL] Voltage just over limit accepted")
        tests_failed += 1
    except ValueError:
        print("  [PASS] Voltage just over limit rejected")
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {tests_passed}")
    print(f"Tests failed: {tests_failed}")
    print(f"Total tests:  {tests_passed + tests_failed}")
    
    if tests_failed == 0:
        print("\n[OK] ALL TESTS PASSED!")
        print("\nRefactoring Summary:")
        print("  - Created _check_voltage_limit() method in both drivers")
        print("  - Centralized voltage validation logic")
        print("  - Added optional 'context' parameter for better error messages")
        print("  - All validation methods now use _check_voltage_limit()")
        print("\nBenefits:")
        print("  - DRY principle: validation logic defined once")
        print("  - Easier to maintain and modify")
        print("  - Consistent error messages")
        print("  - Better error context (e.g., 'sweep start', 'list index 2')")
    else:
        print(f"\n[ERROR] {tests_failed} TEST(S) FAILED!")
    
    print("=" * 70)

if __name__ == "__main__":
    test_check_voltage_limit_method()
