import sqlite3
from datetime import datetime, timedelta
from apscheduler.triggers.interval import IntervalTrigger

from app import db_file


def check_sched_deposit(
    params, user_id, user_status, account_type, last_deposit_id, amount, date
):
    db = params["db"].conn.cursor()
    py_date = datetime.strptime(date, "%Y-%m-%d").date()
    today = datetime.today().date()
    db.execute(
        """SELECT interest_start FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
        (account_type,),
    )
    intr_start = db.fetchone()[0]
    ins = intr_start.split(" ")
    time = ins[1].lower().replace("(s)", "")

    if time == "year":
        time = 52.143 * int(ins[0])
    elif time == "month":
        time = 4.345 * int(ins[0])

    if user_status.lower() == "active":
        interest_start = (
            py_date + timedelta(weeks=time)
            if not py_date < today
            else today + timedelta(days=1)
        )
        deposit_interval = IntervalTrigger(
            days=1,
            start_date=interest_start.strftime("%Y-%m-%d %H:%M:%S"),
        )
        params["qtsched"].add_job(
            interest_schedule,
            trigger=deposit_interval,
            args=[
                user_id,
                last_deposit_id,
            ],
            id=f"dep_{last_deposit_id} interest schedule",
            replace_existing=True,
        )


def interest_schedule(user_id, deposit_id):
    conn = sqlite3.connect(db_file)

    db = conn.cursor()
    db.execute("""SELECT account_type, status FROM users WHERE id=?;""", (user_id,))
    account = db.fetchone()
    account_type = account[0]
    status = account[1]

    if status == "active":
        db.execute(
            """SELECT * FROM deposit_interest WHERE deposit_id=? AND user_id=?;""",
            (deposit_id, user_id),
        )
        deposit_interest = db.fetchone()

        if not deposit_interest is None:
            run_time = deposit_interest[6]
            run_time += 1
            date_added = deposit_interest[3]
            date_elapsed = datetime.strptime(date_added, "%Y-%m-%d").date() + timedelta(
                days=run_time
            )
            amount = deposit_interest[1]

            db.execute(
                """SELECT interest_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                (account_type,),
            )
            interest_rate = db.fetchone()[0]
            interest_rate_per_day = float(interest_rate) / 100 / 365

            interest_per_day = float(deposit_interest[2])
            cal = 0
            db.execute(
                """SELECT interest_earned, total FROM savings WHERE user_id=?;""",
                (user_id,),
            )
            sav_intr = db.fetchone()
            intr_earned = sav_intr[0]
            total = sav_intr[1]

            if interest_per_day == 0.0:
                db.execute(
                    """SELECT interest_start FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                    (account_type,),
                )
                intr_start = db.fetchone()[0]
                ins = intr_start.split(" ")
                time = ins[1].lower().replace("(s)", "")

                if time == "year":
                    time = 365 * int(ins[0])
                elif time == "month":
                    time = 30.417 * int(ins[0])

                _months = time
                _months_interest = _months * interest_rate_per_day * float(amount)

                interest_per_day += _months_interest

                db.execute(
                    """UPDATE deposit_interest SET
                        interest=?,
                        date_interest_start=?,
                        date_last_interest=?,
                        run_time=? WHERE deposit_id=? AND user_id=?;
                    """,
                    (
                        round(interest_per_day),
                        date_elapsed.strftime("%Y-%m-%d"),
                        date_elapsed.strftime("%Y-%m-%d"),
                        run_time,
                        deposit_id,
                        user_id,
                    ),
                )
                intr_earned += round(interest_per_day)
                total += round(interest_per_day)
            else:
                cal = float(amount) * float(interest_rate_per_day)
                interest_per_day += cal

                db.execute(
                    """UPDATE deposit_interest SET
                        interest=?,
                        date_last_interest=?,
                        run_time=? WHERE deposit_id=? AND user_id=?;""",
                    (
                        round(interest_per_day),
                        date_elapsed.strftime("%Y-%m-%d"),
                        run_time,
                        deposit_id,
                        user_id,
                    ),
                )

                intr_earned += round(cal)
                total += round(cal)

            db.execute(
                """UPDATE savings SET
                    interest_earned=?,
                    total=?,
                    date_updated=? WHERE user_id=?;""",
                (
                    round(intr_earned),
                    round(total),
                    date_elapsed.strftime("%Y-%m-%d %H:%M:%S"),
                    user_id,
                ),
            )

            conn.commit()
            db.close()


def check_sched_loan(params, user_id, name, start_date, end_date):
    db = params["db"].conn.cursor()

    db.execute(
        """SELECT id FROM loans WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
        (user_id,),
    )
    loan_id = db.fetchone()[0]
    today = datetime.today().date()

    if not start_date < today:
        loan_interval = IntervalTrigger(
            weeks=4.345,
            start_date=start_date,
            end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
        )
        params["qtsched"].add_job(
            loan_schedule,
            trigger=loan_interval,
            args=[
                user_id,
                loan_id,
            ],
            id=f"{name} loan schedule",
            replace_existing=True,
        )
    else:
        num_mon = today - start_date
        num_mon = num_mon.days / 30.417
        num_mon = round(num_mon)
        db.execute("""SELECT account_type, status FROM users WHERE id=?;""", (user_id,))
        account = db.fetchone()
        db.execute(
            """SELECT loan_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
            (account[0],),
        )
        loan_rate = db.fetchone()[0]

        db.execute(
            """SELECT * FROM loans
                WHERE id=? AND user_id=?;""",
            (
                loan_id,
                user_id,
            ),
        )
        loan = db.fetchone()

        if not loan is None:
            amount = loan[1]
            old_curr_lia = loan[5]

            due_date = datetime.strptime(loan[8], "%Y-%m-%d").date()
            date_issued = datetime.strptime(loan[9], "%Y-%m-%d").date()
            run_time = due_date - date_issued
            run_time = run_time.days / 30.417

            interest_per_month = float(amount) * int(loan_rate) / 100 * round(run_time)
            new_curr_lia = float(old_curr_lia) + float(interest_per_month)

            db.execute(
                """UPDATE loans SET
                    current_liability=?, run_time=?
                    WHERE id=? AND user_id=?;""",
                (
                    new_curr_lia,
                    round(run_time),
                    loan_id,
                    user_id,
                ),
            )

            db.execute(
                """UPDATE users SET
                    status=? WHERE id=?""",
                ("inactive", user_id),
            )

            params["db"].conn.commit()


def loan_schedule(user_id, loan_id):
    conn = sqlite3.connect(db_file)
    db = conn.cursor()

    db.execute("""SELECT account_type, status FROM users WHERE id=?;""", (user_id,))
    account = db.fetchone()
    db.execute(
        """SELECT loan_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
        (account[0],),
    )
    loan_rate = db.fetchone()[0]

    db.execute(
        """SELECT * FROM loans
            WHERE id=? AND user_id=?;""",
        (
            loan_id,
            user_id,
        ),
    )
    loan = db.fetchone()

    if not loan is None:
        amount = loan[1]
        old_curr_lia = loan[5]
        loan_period = loan[7].split(" ")
        time = loan_period[1].lower().replace("(s)", "")

        if time == "year":
            time = 52.143 * int(loan_period[0])
        elif time == "month":
            time = 4.345 * int(loan_period[0])

        time = timedelta(weeks=time).days

        due_date = datetime.strptime(loan[8], "%Y-%m-%d").date()
        date_issued = datetime.strptime(loan[9], "%Y-%m-%d").date()
        run_time = loan[10]
        run_time += 1
        run_time_days = run_time * 30.417

        days_elapsed = date_issued + timedelta(days=run_time_days)

        interest_per_month = float(amount) * int(loan_rate) / 100
        new_curr_lia = float(old_curr_lia) + float(interest_per_month)

        if days_elapsed.days == time:
            db.execute(
                """UPDATE users SET
                    status=? WHERE id=?""",
                ("inactive", user_id),
            )

        db.execute(
            """UPDATE loans SET
                current_liability=?, run_time=? WHERE id=? AND user_id=?;""",
            (
                new_curr_lia,
                round(run_time),
                loan_id,
                user_id,
            ),
        )
        conn.commit()
        db.close()
