from dataclasses import dataclass
import json
import os
import logging
from typing import List


@dataclass
class Person:
    id: int
    first_name: str
    manager: int
    salary: int

    def __post_init__(self):
        self.children = []
        self.keys = []

    def headcount(self):
        return len(self.keys)

    def show(self, level=0):
        space = "  " * level
        print(f"{space}{self.first_name}")
        if len(self.children) > 0:
            print(f"{space}Employees of {self.first_name}")
            for p in self.children:
                p.show(level + 1)

    def total_salary(self):
        total = 0
        for p in self.children:
            total += p.total_salary()
        return self.salary + total


class Tree:
    root: Person
    unlinked: List

    def __init__(self):
        self.root = None
        self.keys = []
        self.unlinked = []

    def headcount(self):
        return len(self.keys)

    def find_person(self, id: int, node: Person) -> Person:
        if not node:
            # if root is null
            return None
        if node.id == id:
            return node
        else:
            # recurring search in the child nodes
            for n in node.children:
                p = self.find_person(id, n)
                if p:
                    return p
        #  if not in the tree
        return None

    def clear_unassigned(self):
        for p in self.unlinked:
            manager = self.find_person(p.manager, self.root)
            if manager:
                self.keys.append(p.id)
                manager.keys.append(p.id)
                manager.children.append(p)
                self.unlinked.remove(p)
                logging.info(f"{p.first_name} cleared from unlinked cache")

    def add_person(self, p: Person) -> bool:
        if p.id in self.keys:
            raise Exception(f"Duplicate ID {p.id}")
        if p.manager == None or p.manager == 0:
            if self.root:
                raise Exception("There is already a CEO exists!")
            self.root = p
            self.keys.append(p.id)
            self.clear_unassigned()
            return True
        else:
            manager = self.find_person(p.manager, self.root)
            if manager:
                self.keys.append(p.id)
                manager.keys.append(p.id)
                manager.children.append(p)
                # after adding new node checking unlinked nodes
                self.clear_unassigned()
                return True
            else:
                logging.warning(f"Manager not found for {p.first_name}")
                # adding object to unlinked pool if there is no parent object
                self.unlinked.append(p)
                return False

    def load_file(self, filename):
        if not os.access(filename, os.R_OK):
            message = f"File {filename} is not readable!"
            raise Exception(message)
        with open(filename) as f:
            data = json.load(f)
        for item in data:
            if self.add_person(Person(**item)):
                logging.info(f"{item} added")
        self.clear_unassigned()
        if len(self.unlinked) > 0:
            for p in self.unlinked:
                logging.error(f"There is no manager found for {p.first_name}")
            raise Exception("There are unlinked nodes")

    def show(self):
        if self.root:
            self.root.show()

    def total_salary(self):
        return self.root.total_salary() if self.root else 0
