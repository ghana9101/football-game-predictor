import json

with open('bob_generated_code.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
print(f"Total cells in notebook: {len(cells)}")
print("\nLast 3 cells:")

for i, cell in enumerate(cells[-3:], len(cells)-2):
    cell_type = cell['cell_type']
    if cell_type == 'markdown':
        content = ''.join(cell['source'])[:80]
    else:
        content = ''.join(cell['source'][:2])[:80]
    print(f"\nCell {i}:")
    print(f"  Type: {cell_type}")
    print(f"  Content: {content}...")

# Check specifically for Task 9
task9_found = False
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'markdown':
        content = ''.join(cell['source'])
        if 'Task 9' in content:
            task9_found = True
            print(f"\n✓ Task 9 found at cell index {i}")
            print(f"  Content: {content}")

if not task9_found:
    print("\n✗ Task 9 heading not found")
else:
    print("\n✓ Task 9 is present in the notebook!")

# Made with Bob
