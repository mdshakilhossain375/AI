from openai import OpenAI
from pathlib import Path
import pandas as pd

BASE = Path.home() / "ShakilAI"
WORKSPACE = BASE / "workspace"
WORKSPACE.mkdir(parents=True, exist_ok=True)

client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama"
)

SYSTEM = """You are Shakil AI, a practical personal assistant for an ESL teacher,
acting headteacher, researcher and family planner.

You can help with:
teaching, school administration, students, research, CELTA, IELTS,
documents, Excel, planning and educational projects.

If the user asks for an Excel file, use one of these exact commands:

EXCEL: ATTENDANCE | filename | number_of_students
EXCEL: MARKSHEET | filename | number_of_students

For normal questions, answer normally.

Never claim an Excel file was created unless the program confirms it.
"""

messages = [{"role": "system", "content": SYSTEM}]

def create_attendance(filename, n):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "Student_ID": f"S{i:03d}",
            "Student_Name": f"Student {i}",
            "Present": "",
            "Absent": "",
            "Late": "",
            "Remarks": ""
        })

    df = pd.DataFrame(rows)
    path = WORKSPACE / filename
    df.to_excel(path, index=False)
    return path

def create_marksheet(filename, n):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "Student_ID": f"S{i:03d}",
            "Student_Name": f"Student {i}",
            "English": "",
            "Bangla": "",
            "Mathematics": "",
            "Science": "",
            "ICT": "",
            "Total": "",
            "Average": "",
            "Grade": ""
        })

    df = pd.DataFrame(rows)
    path = WORKSPACE / filename
    df.to_excel(path, index=False)
    return path

print("=" * 55)
print("             SHAKIL AI")
print("      Excel + File Control Enabled")
print("=" * 55)
print("Type 'exit' to stop.")
print()

while True:
    try:
        user = input("You: ").strip()

        if not user:
            continue

        if user.lower() in ["exit", "quit"]:
            print("Shakil AI closed.")
            break

        messages.append({"role": "user", "content": user})

        response = client.chat.completions.create(
            model="qwen3:4b-instruct",
            messages=messages,
            temperature=0.2
        )

        answer = response.choices[0].message.content.strip()

        if answer.startswith("EXCEL:"):
            parts = [x.strip() for x in answer.split("|")]

            try:
                command = parts[0].replace("EXCEL:", "").strip()
                filename = parts[1]
                number = int(parts[2])

                if not filename.lower().endswith(".xlsx"):
                    filename += ".xlsx"

                if command == "ATTENDANCE":
                    path = create_attendance(filename, number)
                    print(f"\n[OK] Excel file created:")
                    print(path)

                elif command == "MARKSHEET":
                    path = create_marksheet(filename, number)
                    print(f"\n[OK] Excel file created:")
                    print(path)

                else:
                    print("\n[Agent] Unknown Excel command.")

            except Exception as e:
                print(f"\n[Excel Error] {e}")

        else:
            print(f"\nShakil AI: {answer}\n")

        messages.append({"role": "assistant", "content": answer})

    except KeyboardInterrupt:
        print("\nShakil AI closed.")
        break

    except Exception as e:
        print(f"\nError: {e}\n")
