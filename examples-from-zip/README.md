# Example Files from ProtoQSAR

These files were extracted from script.zip and contain working examples of API usage:

## Files

1. **API-Request_ONTOXHub_json.py** - Python script showing different API request options:
   - Option 1: Single SMILES as text input
   - Option 2: File upload (Excel or JSON)
   - Option 3: Embedded JSON in request
   - Option 4: Excel output format

2. **JSON_input.json** - Example JSON file format for batch predictions with multiple molecules

3. **request_body_API.json** - Example of full request body with embedded JSON data

4. **input.xlsx** - Example Excel file for batch upload

## Important Notes

- These files contain the working API credentials
- They demonstrate the correct request format that the API expects
- The API endpoint is: `https://protopred.protoqsar.com/API/v2/`
- Requests should use form-encoded data (not JSON body) except for embedded JSON option