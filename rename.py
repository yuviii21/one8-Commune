import os

directory = r'c:\Users\gyuva\Downloads\meal\FinalMealmate\delivery\templates\delivery'
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace app name
            new_content = content.replace('Meal Buddy', 'one8 Commune')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {file}")

print("Replacement complete.")
