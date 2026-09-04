"""Database testing with sqlite3 (stdlib) — CRUD, constraints, transactions, integrity."""
import logging
import sqlite3

import pytest

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("db-tests")


@pytest.fixture()
def db():
    """In-memory sqlite db with users/orders schema, FK enforcement on."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        );
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            amount REAL NOT NULL CHECK(amount >= 0),
            status TEXT NOT NULL DEFAULT 'pending'
        );
        """
    )
    log.info("schema created: users, orders (foreign_keys=ON)")
    yield conn
    conn.close()
    log.info("connection closed")


# ---------- CRUD ----------

def test_insert_and_read_user(db):
    cur = db.execute("INSERT INTO users (email, name) VALUES (?, ?)", ("a@x.com", "Alice"))
    uid = cur.lastrowid
    db.commit()
    row = db.execute("SELECT email, name FROM users WHERE id=?", (uid,)).fetchone()
    log.info("inserted user id=%s -> %s", uid, row)
    assert row == ("a@x.com", "Alice")


def test_update_user(db):
    uid = db.execute("INSERT INTO users (email, name) VALUES ('b@x.com','Bob')").lastrowid
    db.execute("UPDATE users SET name=? WHERE id=?", ("Bobby", uid))
    db.commit()
    name = db.execute("SELECT name FROM users WHERE id=?", (uid,)).fetchone()[0]
    log.info("updated user id=%s name=%s", uid, name)
    assert name == "Bobby"


def test_delete_user(db):
    uid = db.execute("INSERT INTO users (email, name) VALUES ('c@x.com','Cid')").lastrowid
    db.execute("DELETE FROM users WHERE id=?", (uid,))
    db.commit()
    count = db.execute("SELECT COUNT(*) FROM users WHERE id=?", (uid,)).fetchone()[0]
    log.info("deleted user id=%s remaining=%s", uid, count)
    assert count == 0


# ---------- Constraints ----------

def test_unique_email_constraint(db):
    db.execute("INSERT INTO users (email, name) VALUES ('dup@x.com','One')")
    db.commit()
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO users (email, name) VALUES ('dup@x.com','Two')")
    log.info("UNIQUE constraint on users.email enforced")


def test_foreign_key_constraint(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO orders (user_id, amount) VALUES (999, 10.0)")
    log.info("FOREIGN KEY orders.user_id -> users.id enforced")


def test_check_amount_non_negative(db):
    uid = db.execute("INSERT INTO users (email, name) VALUES ('d@x.com','Dee')").lastrowid
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO orders (user_id, amount) VALUES (?, -5)", (uid,))
    log.info("CHECK amount >= 0 enforced")


# ---------- Transactions ----------

def test_transaction_rollback(db):
    db.execute("INSERT INTO users (email, name) VALUES ('e@x.com','Eve')")
    db.commit()
    try:
        db.execute("INSERT INTO orders (user_id, amount) VALUES (1, 20.0)")
        raise RuntimeError("simulated mid-transaction failure")
    except RuntimeError:
        db.rollback()
        log.info("rolled back transaction after simulated failure")
    count = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    assert count == 0


# ---------- Data integrity ----------

def test_order_totals_per_user(db):
    u1 = db.execute("INSERT INTO users (email,name) VALUES ('f1@x.com','F1')").lastrowid
    u2 = db.execute("INSERT INTO users (email,name) VALUES ('f2@x.com','F2')").lastrowid
    db.executemany(
        "INSERT INTO orders (user_id, amount, status) VALUES (?,?,?)",
        [(u1, 10.0, "done"), (u1, 15.5, "done"), (u2, 7.25, "done")],
    )
    db.commit()
    rows = db.execute(
        "SELECT u.email, SUM(o.amount) FROM users u "
        "JOIN orders o ON o.user_id = u.id GROUP BY u.id ORDER BY u.email"
    ).fetchall()
    log.info("order totals per user: %s", rows)
    assert rows == [("f1@x.com", 25.5), ("f2@x.com", 7.25)]
