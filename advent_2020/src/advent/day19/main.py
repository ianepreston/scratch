"""Day 19 of the advent of code challenge."""
from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple


class Rule(NamedTuple):
    """I'm  a message rule."""

    id: int
    literal: Optional[str] = None
    child_rules: List[List[int]] = []


def parse_rule(line: str) -> Rule:
    """Generate a rule.

    Parameters
    ----------
    line: str
        input line representing a rule
    
    Returns
    -------
    Rule
        The parsed rule
    """
    id, rules = line.strip().split(": ")
    if rules.startswith('"'):
        return Rule(id=int(id), literal=rules.replace('"', ""))
    choices = rules.split("|")
    return Rule(
        id=int(id), child_rules=[[int(n) for n in choice.split()] for choice in choices]
    )


def read_inputs(filename: str) -> Tuple[Dict[int, Rule], List[str]]:
    """Read in a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module


    Returns
    -------
    rules_dict, messages
        dictionary of rule ids mapped to rule objects and a list of messages
    """
    here: Path = Path(__file__).resolve().parent
    in_path: Path = here / filename
    with open(in_path, "r") as f:
        rules_str: str
        messages_str: str
        rules_str, messages_str = f.read().split("\n\n")
    rules_dict: Dict[int, Rule] = {
        rule.id: rule
        for rule in (parse_rule(ruleline) for ruleline in rules_str.split("\n"))
    }
    messages: List[str] = [message for message in messages_str.split("\n")]
    return rules_dict, messages


def check_message(rules_dict: Dict[int, Rule], message: str) -> bool:
    """Check if a message is valid.
    
    Parameters
    ----------
    rules_dict: Dict[int, Rule]
        map rule ids to Rule objects
    message: str
        The message to validate
    
    Returns
    -------
    bool:
        Whether or not the message is valid
    """
    # make a queue of
    q = deque([(message, [0])])
    while q:
        # take from the queue
        message, rule_ids = q.popleft()

        # If we have an empty string and an empty list
        # we've consumed both the entire message and all the
        # rules, so that's a match
        if not message and not rule_ids:
            return True

        # If we have consumed the string or the rules but not both -> no match
        elif not message or not rule_ids:
            continue

        # Each rule matches at least 1 character, if we have more rules than characters
        # it can't be a match
        elif len(rule_ids) > len(message):
            continue

        # have both a remaining message and rule_ids.
        # Try the first rule and remove it from the list of rules to try
        rule = rules_dict[rule_ids[0]]
        rule_ids = rule_ids[1:]

        # first rule is literal, so if it matches the first character,
        # then add the rest of the string and the rest of the rules to the queue
        if rule.literal and message[0] == rule.literal:
            q.append((message[1:], rule_ids))

        # otherwise, I have one more sequences of subrules,
        # for each of those sequences, I prepend it to the remaining rule_ids
        # and add that new list of rule ids to the queue with s
        else:
            for subrule_ids in rule.child_rules:
                q.append((message, subrule_ids + rule_ids))

    # queue is exhausted, never found a match, so return False
    return False


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the challenge.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module

    Returns
    -------
    int
        The answer to part 1
    """
    rules_dict, messages = read_inputs(filename)
    return sum(check_message(rules_dict, message) for message in messages)


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the challenge.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module

    Returns
    -------
    int
        The answer to part 2
    """
    rules_dict, messages = read_inputs(filename)
    rules_dict[8] = parse_rule("8: 42 | 42 8")
    rules_dict[11] = parse_rule("11: 42 31 | 42 11 31")
    return sum(check_message(rules_dict, message) for message in messages)


if __name__ == "__main__":
    part1("example.txt")
