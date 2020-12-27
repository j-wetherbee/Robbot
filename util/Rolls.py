import re
import random


def rolls_from_args(args: str):
    if _DNDRoll.args_match_regex(args):
        ret = _DNDRoll(args)
    elif _RangeRoll.args_match_regex(args):
        ret = _RangeRoll(args)
    elif _ListRoll.args_match_regex(args):
        ret = _ListRoll(args)
    elif args == '':
        ret = _RangeRoll('1-100')
    else:
        ret = None
    
    return str(ret) if ret else None


# TODO this might be better than the abstract roll class? clear that it doesn't stand alone, and not every roller needs to use it
class _RollUtil():
    @classmethod
    def _args_match_regex(cls, pattern: str, args: str):
        match = re.search(pattern, args)
        return True if match else False
    
    @classmethod
    def _findall_matches_in_args(cls, pattern: str, args: str):
        matches = re.findall(pattern, args)
        return matches

    @classmethod
    def parse_args_and_roll(cls, roller, args: str):
        pattern = roller._arg_pattern
        matches = cls._findall_matches_in_args(pattern, args)
        roller._parse_matches(matches)
        roller.roll()

class _AbstractRoll():
    _arg_pattern = None

    @classmethod
    def _args_match_regex(cls, pattern: str, args: str):
        match = re.search(pattern, args)
        return True if match else False

    def __init__(self, args: str):
        matches = self._findall_matches_in_args(args)
        self._parse_matches(matches)
        self.roll()
    
    def _findall_matches_in_args(self, args: str):
        matches = re.findall(self._arg_pattern, args)
        return matches

    def _parse_matches(self, matches):
        pass

    def roll(self):
        pass

class _DNDRoll(_AbstractRoll):  # Names TBD
    _arg_pattern = r'([0-9]*d[0-9]+)(\+[0-9]+)*'

    @classmethod
    def args_match_regex(cls, args: str):  # TODO this code is repeated in each subclass - feel like there should be a way to put it all in the abstract and work out the arg_pattern problem with a factory?
        return super()._args_match_regex(cls._arg_pattern, args)

    def __init__(self, args: str):
        self.rolls = []
        super().__init__(args)

    def _parse_matches(self, matches):
        def parse_num_rolls(roll_match):
            roll_parts = roll_match.split('d')
            num_rolls = roll_parts[0]
            if not num_rolls:
                num_rolls = 1
            return int(num_rolls)

        def parse_max_roll(roll_match):
            roll_parts = roll_match.split('d')
            max_roll = roll_parts[-1]
            return int(max_roll)

        def parse_offset(offset_match):
            offset_parts = offset_match.split('+')
            offset = offset_parts[-1]
            if not offset:
                offset = 0
            return int(offset)

        for match in matches:
            roll_match, offset_match = match

            num_rolls = parse_num_rolls(roll_match)
            max_roll = parse_max_roll(roll_match)
            offset = parse_offset(offset_match)

            roll = {'num': num_rolls, 'max': max_roll, 'offset': offset}
            self.rolls.append(roll)

    def roll(self):
        for roll in self.rolls:
            num_rolls = roll['num']
            max_roll = roll['max']
            offset = roll['offset']

            sub_rolls = [random.randint(1, max_roll) for _ in range(num_rolls)]
            result = sum(sub_rolls) + offset

            roll['sub_rolls'] = sub_rolls
            roll['result'] = result

    def __str__(self):
        rolls = []
        for roll in self.rolls:
            num_rolls = str(roll['num'])
            max_roll = str(roll['max'])
            offset = str(roll['offset'])
            result = str(roll['result'])
            sub_rolls = [str(sub_roll) for sub_roll in roll['sub_rolls']]

            sub_rolls = ' + '.join(sub_rolls)
            rolls.append(f"{num_rolls}d{max_roll}: {sub_rolls} + {offset} = {result}")
        return '\n'.join(rolls)

    
class _RangeRoll(_AbstractRoll):  # Names TBD
    _arg_pattern = r'[0-9]+-[0-9]+'

    @classmethod
    def args_match_regex(cls, args: str):
        return super()._args_match_regex(cls._arg_pattern, args)

    def __init__(self, args: str):
        self.rolls = []
        super().__init__(args)
        
    def _parse_matches(self, matches):
        for match in matches:
            bounds = match.split('-')
            bounds = [int(bound) for bound in bounds]
            low = min(bounds)
            high = max(bounds)
            
            self.rolls.append({'min': low, 'max': high})

    def roll(self):
        for roll in self.rolls:
            result = random.randint(roll['min'], roll['max'])
            roll['result'] = result

    def __str__(self):
        rolls = [f"{roll['min']}-{roll['max']}: {roll['result']}" for roll in self.rolls]
        return '\n'.join(rolls)


class _ListRoll(_AbstractRoll):  # Names TBD
    _arg_pattern = r'\w+'

    @classmethod
    def args_match_regex(cls, args: str):
        return super()._args_match_regex(cls._arg_pattern, args)

    def __init__(self, args: str):
        self.choices = []
        self.result = None
        super().__init__(args)

    def _parse_matches(self, matches):
        self.choices = matches

    def roll(self):
        self.result = random.choice(self.choices)

    def __str__(self):
        choices_str = "Choices: " + ", ".join(self.choices)
        result_str = f"Result: {self.result}"
        return f"{choices_str}\n{result_str}"

