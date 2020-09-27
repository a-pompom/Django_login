import pytest # type: ignore

from django.core.exceptions import ValidationError

from ..validator import *

class TestValidatorMinLength:
    """ 最小文字数チェック """

    @pytest.mark.parametrize(
        'value,length',
        [
        pytest.param('text', 3, id='More than min length'),
        pytest.param('justText', 8, id='Equal to min length'),
        pytest.param('日本語の長さ', 6, id='Japanese character')
        ]
    )
    def test_最小文字数を満たすと例外が送出されないこと(self, value: str, length: int):

        try:
            validate_min_length(value, length)
        except ValidationError:
            pytest.fail('invalid value')

    @pytest.mark.parametrize(
        'value,length',
        [
            pytest.param('pompom', 7, id='One character lack'),
            pytest.param('purin', 999, id='Far lack'),
            pytest.param('これは文字です', 8, id='Jpanese String lack')
        ]
    )
    def test_最小文字数を満たさないと例外が送出されること(self, value: str, length: int):

        with pytest.raises(ValidationError):
            validate_min_length(value, length)

class TestValidatorMaxLength:
    """ 最大文字長チェック """

    @pytest.mark.parametrize(
        'value,length',
        [
        pytest.param('tdd', 4, id='Less than max length'),
        pytest.param('justText', 8, id='Equal to max length'),
        pytest.param('日本語の長さ', 6, id='Japanese character')
        ]
    )
    def test_最大文字数を満たすと例外が送出されないこと(self, value: str, length: int):
        try:
            validate_max_length(value, length)
        except ValidationError:
            pytest.fail('invalid value')


    @pytest.mark.parametrize(
        'value,length',
        [
            pytest.param('pompom', 5, id='One character over'),
            pytest.param('pompom purin', 5, id='Far over'),
            pytest.param('これは文字です', 3, id='Jpanese String over')
        ]
    )
    def test_最大文字数を超過すると例外が送出されること(self, value: str, length: int):

        # THEN
        with pytest.raises(ValidationError):
            validate_max_length(value, length)

class TestValidatorAlphaNumeric:
    """ 文字種別チェック """

    @pytest.mark.parametrize(
        'value',
        [
            pytest.param('a-pompom', id='Common character'),
            pytest.param('A-pompom_1234', id='FullType character'),
            pytest.param('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', id='All character'),
        ]
    )
    def test_半角英数とハイフンアンダースコアを含む文字列を渡すと例外が送出されないこと(self, value: str):
        try:
            validate_alpha_numeric(value)
        except ValidationError:
            pytest.fail('invalid value')


    @pytest.mark.parametrize(
        'value',
        [
            pytest.param('user a-pompom', id='Include space'),
            pytest.param('#user^', id='Invalid symbol'),
            pytest.param('日本語文字列', id='Japanese character'),
        ]
    )
    def test_指定文字種以外を渡すと例外が送出されること(self, value: str):

        # THEN
        with pytest.raises(ValidationError):
            validate_alpha_numeric(value)