import re
from typing import Callable, Any

from django.core.exceptions import ValidationError

def get_validator(validation_function: Callable, *args: Any) -> Callable:
    """ validation処理を実行する関数を取得

    Parameters
    ----------
    validation_function : Callable
        バリデーションエラーとなるとき、ValidationErrorを送出する関数

    Returns
    -------
    Callable
        DjangoのFieldから実際に呼ばれるバリデーション関数
    """

    return lambda value: validation_function(value, *args)

def validate_min_length(value: str, length: int):
    """ 最小文字数チェック

    Parameters
    ----------
    value : str
        検査対象文字列
    length : int
        許容される最小文字数
    message: str
        エラーメッセージ
    """

    if len(value) < length:
        raise ValidationError(f'{length}文字以上で入力してください。')

def validate_max_length(value: str, length: int):
    """ 最小文字数チェック

    Parameters
    ----------
    value : str
        検査対象文字列
    length : int
        許容される最小文字数
    message: str
        エラーメッセージ
    """

    if len(value) > length:
        raise ValidationError(f'{length}文字以下で入力してください。')


def validate_alpha_numeric(value: str):
    """ 文字列が半角英数と-_で構成されているか

    Parameters
    ----------
    value : str
        検査対象文字列

    Returns
    -------
    bool
        True -> 文字列が半角英数-_のみからなる
        False -> 文字列に半角英数-_以外が含まれる or 空文字
    """    

    if re.search('^[0-9a-zA-Z-_]+$', value) is None:
        raise ValidationError('半角英数または「-_」のみ使用できます。')