from datetime import date


def test_advance_purchase_thirteen_fourteen_and_fifteen_day_boundary(book_adult, memory_store):
    memory_store.clock.today = date(2030, 1, 2)
    assert book_adult()["total_fare"] == 700
    memory_store.clock.today = date(2030, 1, 1)
    assert book_adult()["total_fare"] == 595
    memory_store.clock.today = date(2029, 12, 31)
    assert book_adult()["total_fare"] == 595


def test_corporate_advance_uses_best_single_discount(book_adult, memory_store):
    memory_store.clock.today = date(2030, 1, 1)
    assert book_adult(member_id="M002")["total_fare"] == 595
    assert book_adult()["total_fare"] == 595
