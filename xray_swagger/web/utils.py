import json
from typing import Any, LiteralString, Sequence

from diff_match_patch import diff_match_patch, patch_obj
from loguru import logger

dmp = diff_match_patch()


class PatchRevertUnsuccessful(Exception):
    ...


def make_patch_text(old: Any, new: Any) -> LiteralString:
    old = json.dumps(old)
    new = json.dumps(new)

    print("SHOW TWO ITEMS".center(60, "*"))
    print(f"{old=}")
    print(f"{new=}")

    print("  PATCH old -> new  ".center(60, "*"))
    patches = dmp.patch_make(old, new)
    patches_text = dmp.patch_toText(patches)
    return patches_text


def revert_diffs(diffs):
    # DIFF_DELETE = -1
    # DIFF_INSERT = 1
    # DIFF_EQUAL = 0
    def revert_diff(diff):
        flag, string = diff
        if flag == diff_match_patch.DIFF_EQUAL:
            return flag, string
        return flag * -1, string

    reverted_diffs = [revert_diff(d) for d in diffs]

    return reverted_diffs


def revert_patches(patches) -> Sequence[patch_obj]:
    patches = dmp.patch_deepCopy(patches)
    for p in patches:
        p.diffs = revert_diffs(p.diffs)
    return patches


def make_reverted_patch_from_patch_text(patch_text: str) -> Sequence[patch_obj]:
    patches_from_text = dmp.patch_fromText(patch_text)
    logger.debug(patches_from_text)
    rpatches = revert_patches(patches_from_text)

    return rpatches


def apply_patch_revert(b: Any, patch_text: str):
    print("Revert PATCH b->a".center(60, "*"))
    _b = json.dumps(b)
    rpatches = make_reverted_patch_from_patch_text(patch_text)
    logger.debug(rpatches)
    rpatched_b_to_a = dmp.patch_apply(rpatches, _b)
    patch_result, validations = rpatched_b_to_a
    print(patch_result)
    if not all(validations):
        raise PatchRevertUnsuccessful

    return json.loads(patch_result)
