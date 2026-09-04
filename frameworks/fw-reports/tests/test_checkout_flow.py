"""Checkout-flow tests for the fw-reports showcase.

Also generates a small PNG file (a stand-in "screenshot") into out/ so
uploadArtefacts has a binary artefact to show in the UI.
"""
import base64
import os
import time

import pytest

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
LOG = os.path.join(OUT, "execution.log")

# 1x1 red pixel PNG
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4"
    "z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg=="
)


def _log(msg):
    os.makedirs(OUT, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] test_checkout_flow :: {msg}\n")


def test_add_to_cart():
    _log("add item to cart")
    with open(os.path.join(OUT, "screenshot-add-to-cart.png"), "wb") as f:
        f.write(TINY_PNG)
    assert True


def test_apply_coupon():
    _log("apply coupon code SAVE10")
    assert True


@pytest.mark.skip(reason="payment gateway sandbox is flaky on stage - showcase skip status")
def test_payment_gateway_charge():
    _log("charge via payment gateway")
    assert True


def test_order_confirmation_email():
    _log("order confirmation email queued")
    assert True
