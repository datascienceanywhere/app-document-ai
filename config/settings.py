try:
    # base path
    import os
    import sys

    base_path = os.path.abspath('.')
    sys.path.append(base_path)

    # import helper
    import helper

except Exception as e:
    print("Running in cloud environment", e)