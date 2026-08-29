import sqlite3
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

DB_PATH = Path("database/student_performance.db")

QA_SQL_PATH = Path("sql/qa_validation.sql")
REPORT_SQL_PATH = Path("sql/reporting_queries.sql")


# ============================================================
# SQL LOADER
# ============================================================

def load_sql_statements(sql_path):
    """
    Read a SQL file and split it into executable statements.
    """

    sql = sql_path.read_text(encoding="utf-8")

    statements = []

    for statement in sql.split(";"):

        statement = statement.strip()

        if not statement:
            continue

        # Remove SQL comment lines
        lines = []

        for line in statement.splitlines():

            if not line.strip().startswith("--"):
                lines.append(line)

        statement = "\n".join(lines).strip()

        if statement:
            statements.append(statement)

    return statements


# ============================================================
# EXECUTE SQL FILE
# ============================================================

def execute_sql_file(conn, sql_path, query_type):

    statements = load_sql_statements(sql_path)

    executed = 0
    failed = 0

    print("\n" + "=" * 60)
    print(query_type)
    print("=" * 60)

    for statement in statements:

        sql_start = statement.upper()

        # Only execute SELECT / WITH queries
        if not (
            sql_start.startswith("SELECT")
            or sql_start.startswith("WITH")
        ):
            continue

        executed += 1

        try:

            cursor = conn.execute(statement)

            rows = cursor.fetchall()

            print(f"\n{query_type} #{executed}")
            print(f"PASS - {len(rows)} row(s) returned")

            # Display first 5 rows only
            for row in rows[:5]:
                print("   ", row)

        except sqlite3.Error as e:

            failed += 1

            print(f"\n{query_type} #{executed}")
            print("FAIL")
            print(f"   Error: {e}")

    return executed, failed


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("STUDENT PERFORMANCE DATABASE")
    print("QA + REPORTING EXECUTION")
    print("=" * 60)

    # Check database
    if not DB_PATH.exists():

        print(f"\nERROR: Database not found:")
        print(f"       {DB_PATH}")

        return

    # Check SQL files
    if not QA_SQL_PATH.exists():

        print(f"\nERROR: QA SQL file not found:")
        print(f"       {QA_SQL_PATH}")

        return

    if not REPORT_SQL_PATH.exists():

        print(f"\nERROR: Reporting SQL file not found:")
        print(f"       {REPORT_SQL_PATH}")

        return

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    try:

        # ----------------------------------------------------
        # QA VALIDATION
        # ----------------------------------------------------

        qa_executed, qa_failed = execute_sql_file(
            conn,
            QA_SQL_PATH,
            "QA VALIDATION"
        )

        # ----------------------------------------------------
        # REPORTING QUERIES
        # ----------------------------------------------------

        report_executed, report_failed = execute_sql_file(
            conn,
            REPORT_SQL_PATH,
            "REPORTING QUERY"
        )

    finally:

        conn.close()

    # ========================================================
    # FINAL RESULT
    # ========================================================

    total_executed = qa_executed + report_executed
    total_failed = qa_failed + report_failed

    print("\n" + "=" * 60)

    print(f"QA validations executed: {qa_executed}")
    print(f"QA validations failed:   {qa_failed}")

    print()

    print(f"Reports executed:        {report_executed}")
    print(f"Reports failed:          {report_failed}")

    print()

    print(f"Total queries executed:  {total_executed}")
    print(f"Total failures:          {total_failed}")

    print("=" * 60)

    if total_failed == 0:

        print("RESULT: ALL QA + REPORTING QUERIES PASSED")

    else:

        print("RESULT: QA/REPORTING EXECUTION FAILED")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()