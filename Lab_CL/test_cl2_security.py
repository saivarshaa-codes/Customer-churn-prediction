import os
import sys
sys.path.insert(0, os.path.abspath("."))

from Lab_CL.prompt_loader import load_template, SecurityLeakageError, ValidationError
from Lab_CL.project_context import PROJECT_CONTEXT, get_system_context

def test_template_loading():
    print("[1/4] Testing valid template loading...")
    prompt = load_template(
        "dataset_profiling_v1",
        dataset_name="Telco Churn Production",
        total_rows=7043,
        columns_list=["customer_id", "tenure", "monthly_charges", "total_charges", "churn"],
        data_summary="7,043 rows, 11 blank TotalCharges, 26.5% churn."
    )
    assert "Telco Churn Production" in prompt
    assert "7043" in prompt
    print("  [OK] Template loaded and rendered properly.")

def test_secret_leakage_prevention():
    print("[2/4] Testing secret-leakage guard (deliberate injection of .env secret)...")
    # Set a mock sensitive key in environment to test detection
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test-super-secret-key-12345"

    secret_injected = False
    try:
        # Deliberately attempt to leak secret into template
        load_template(
            "scaffold_api_endpoint_v1",
            route_path="/test",
            http_method="GET",
            endpoint_purpose="Test endpoint",
            input_spec="None",
            response_spec="dict",
            auth_requirement="Bearer " + os.environ["ANTHROPIC_API_KEY"] # VIOLATION!
        )
    except SecurityLeakageError as e:
        secret_injected = True
        print(f"  [OK] Secret leakage successfully caught and blocked: {e}")

    assert secret_injected, "CRITICAL FAILURE: Secret-leakage guard failed to block env secret!"

def test_argument_validation():
    print("[3/4] Testing argument validation & error handling...")
    missing_param_caught = False
    try:
        # Missing required parameters
        load_template("dataset_profiling_v1", dataset_name="Incomplete Spec")
    except ValidationError:
        missing_param_caught = True
        print("  [OK] Missing parameters caught as ValidationError.")

    assert missing_param_caught, "Validation failed to enforce required template fields!"

def test_project_memory_grounding():
    print("[4/4] Testing project memory grounding...")
    ctx = get_system_context()
    assert "7,043 customers" in ctx
    assert "26.5%" in ctx
    assert "TotalCharges Blanks" in ctx
    assert "v_high_risk_customers" in ctx
    print("  [OK] Project memory verified: Contains data quirks, table names, and ML rules.")

def main():
    print("=" * 60)
    print("RUNNING LAB CL2 SECURITY & PROJECT MEMORY TEST SUITE")
    print("=" * 60)
    test_template_loading()
    test_secret_leakage_prevention()
    test_argument_validation()
    test_project_memory_grounding()
    print("\n" + "=" * 60)
    print("ALL LAB CL2 SECURITY TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
