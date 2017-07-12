import numpy as np
import pytest
from sklearn.exceptions import FitFailedWarning

from sparsereg.model import STRidge

test_settings = (
    dict(threshold=0.5, copy_x=True, normalize=True, fit_intercept=True),
    dict(threshold=0.1, copy_x=True, normalize=False, fit_intercept=True),
    dict(threshold=0.1, alpha=0, copy_x=True, normalize=True, fit_intercept=True),
)


@pytest.mark.parametrize("kw", test_settings)
def test_stridge_normalize(data, kw):
    x, y = data
    s = STRidge(**kw).fit(x, y)

    np.testing.assert_allclose(s.coef_, np.array([0, 2]), atol=1e-7)
    np.testing.assert_allclose(s.predict(x), y)


def test_stridge_knob(data):
    x, y = data
    s = STRidge(normalize=False).fit(x, y)
    assert all(c > s.threshold or c == 0 for c in s.coef_)

def test_all_zero(data):
    x, y = data
    s = STRidge(threshold=10000).fit(x, y)
    assert not any(s.coef_)