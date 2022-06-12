#!/usr/bin/env python3
# coding=utf-8

from dataclasses import dataclass, asdict


@dataclass
class Z:
    name: str
    surname: str
    age: int
    comment: str = ''


z = Z('Dmitrii', 'Gusev', 42)

d = {"name": "Dmitrii-2", "surname": "Gusev-2", "age": 422, "abcd": "123"}
z2 = Z(**d)

print(z)
# print(asdict(z))
print(z2)
