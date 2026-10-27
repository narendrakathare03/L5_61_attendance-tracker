"""Attendance tracker for Lab 5 static code analysis."""

import csv
import os
import tarfile
from pathlib import Path
from typing import Any

import requests

# Global attendance register
students: dict[str, dict[str, Any]] = {}

ERP_URL = os.getenv(
    "ERP_URL",
    "https://erp.college.example/api/attendance",
)
ERP_API_KEY = os.getenv("ERP_API_KEY", "")
MIN_ATTENDANCE = 75


def add_student(roll_no: str, name: str, section: str = "A") -> None:
    """Add a student to the attendance register."""
    students[roll_no] = {
        "name": name,
        "section": section,
        "records": [],
    }


def mark_attendance(
    roll_no: str,
    attendance_date: str,
    status: str,
    register: dict[str, list[str]] | None = None,
) -> dict[str, list[str]]:
    """Record attendance and return the date-wise register."""
    if roll_no not in students:
        raise KeyError(f"Unknown student roll number: {roll_no}")

    if status not in {"P", "A", "L", "H"}:
        raise ValueError("Status must be P, A, L, or H.")

    if register is None:
        register = {}

    register.setdefault(attendance_date, []).append(roll_no)
    students[roll_no]["records"].append((attendance_date, status))

    return register


def attendance_percentage(roll_no: str) -> float:
    """Calculate the percentage of sessions attended."""
    records = students[roll_no]["records"]

    if not records:
        return 0.0

    present = sum(status == "P" for _, status in records)
    return present / len(records) * 100


def is_eligible(percentage: float) -> bool:
    """Check whether attendance meets the minimum requirement."""
    return percentage >= MIN_ATTENDANCE


def shortage_list() -> list[str]:
    """Return students below the required attendance percentage."""
    return [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]


def has_long_absence(roll_no: str, days: int = 3) -> bool:
    """Check whether a student has consecutive absences."""
    if days <= 0:
        raise ValueError("days must be greater than zero")

    statuses = [
        status for _, status in students[roll_no]["records"]
    ]

    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(len(statuses) - days + 1)
    )


def latest_date(roll_no: str) -> str | None:
    """Return the latest attendance date or None if no records exist."""
    dates = [
        record_date
        for record_date, _ in students[roll_no]["records"]
    ]

    return max(dates) if dates else None


def safe_csv_cell(value: object) -> object:
    """Protect exported text fields against spreadsheet formula injection."""
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return "'" + value

    return value


def export_csv(path: str = "attendance.csv") -> str:
    """Export attendance summaries to a CSV file."""
    output_path = Path(path)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["roll_no", "name", "percentage"])

        for roll_no, student in students.items():
            writer.writerow(
                [
                    safe_csv_cell(roll_no),
                    safe_csv_cell(student["name"]),
                    round(attendance_percentage(roll_no), 2),
                ]
            )

    return str(output_path)


def sync_to_erp(roll_no: str) -> int:
    """Send attendance to the configured ERP endpoint."""
    if not ERP_API_KEY:
        raise RuntimeError(
            "Set ERP_API_KEY in the environment before syncing."
        )

    response = requests.post(
        ERP_URL,
        json={
            "roll_no": roll_no,
            "pct": attendance_percentage(roll_no),
        },
        headers={"X-API-Key": ERP_API_KEY},
        timeout=10,
    )

    response.raise_for_status()
    return response.status_code


def backup_reports() -> None:
    """Back up CSV reports without invoking a shell."""
    csv_paths = sorted(Path(".").glob("*.csv"))

    if not csv_paths:
        return

    with tarfile.open("reports_backup.tgz", "w:gz") as archive:
        for csv_path in csv_paths:
            archive.add(csv_path, arcname=csv_path.name)


def run_job(command: list[str]) -> dict[str, Any]:
    """Represent a scheduled command safely as an argument list."""
    if not command or not all(
        isinstance(part, str) for part in command
    ):
        raise ValueError(
            "command must be a non-empty list of strings"
        )

    return {
        "command": command,
        "shell": False,
    }


def schedule_reminders() -> dict[str, Any]:
    """Return a safe reminder-job configuration."""
    return run_job(["send_sms", "--shortage"])


def main() -> None:
    """Run a demonstration of the attendance tracker."""
    add_student("R01", "Aditi")
    add_student(
        "R02",
        '=HYPERLINK("http://evil.example","Bharat")',
    )

    first_records = [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]

    second_records = [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-09-05", "P"),
    ]

    register: dict[str, list[str]] = {}

    for attendance_date, status in first_records:
        register = mark_attendance(
            "R01",
            attendance_date,
            status,
            register,
        )

    for attendance_date, status in second_records:
        register = mark_attendance(
            "R02",
            attendance_date,
            status,
            register,
        )

    print(
        "R01 attendance %:",
        round(attendance_percentage("R01"), 2),
    )
    print(
        "R02 attendance %:",
        round(attendance_percentage("R02"), 2),
    )
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print(
        "Register entries for 2026-09-01:",
        register["2026-09-01"],
    )
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (not requested by demo).")


if __name__ == "__main__":
    main()
