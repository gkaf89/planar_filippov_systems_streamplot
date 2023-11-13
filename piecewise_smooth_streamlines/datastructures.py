from __future__ import annotations
from typing import TypeVar, Generic, Optional, List #, get_type_hints
import unittest

T = TypeVar('T')

class _Node(Generic[T]):
	def __init__(self, data : T, prev : Optional[_Node[T]], next : Optional[_Node[T]]) -> None:
		self.data : T = data
		self.prev : Optional[_Node[T]] = prev
		self.next : Optional[_Node[T]] = next

	@staticmethod
	def empty():
		return _Node(None, None, None)

	@staticmethod
	def create(data, prev, next):
		return _Node(data, prev, next)

class Dequeue(Generic[T]):
	def __init__(self) -> None:
		self.__head : Optional[_Node[T]] = None
		self.__tail : Optional[_Node[T]] = None
	
	def empty(self) -> bool:
		return (self.__head is None) and (self.__tail is None)
	
	def size(self) -> int:
		current : Optional[_Node[T]] = self.__head
		n : int = 0
		while current is not None:
			n = n + 1
			current = current.prev
		
		return n
	
	def push_front(self, data : T) -> None:
		if self.__head is None:
			self.__head = _Node(data, None, None)
			self.__tail = self.__head
		else:
			new_head : _Node[T] = _Node(data, self.__head, None)
			self.__head.next = new_head
			self.__head = new_head
	
	def push_back(self, data : T) -> None:
		if self.__tail is None:
			self.__tail = _Node(data, None, None)
			self.__head = self.__tail
		else:
			new_tail : _Node[T] = _Node(data, None, self.__tail)
			self.__tail.prev = new_tail
			self.__tail = new_tail
	
	def front(self) -> Optional[T]:
		if self.__head is None:
			return None
		else:
			return self.__head.data
	
	def back(self) -> Optional[T]:
		if self.__tail is None:
			return None
		else:
			return self.__tail.data
	
	def pop_front(self) -> Optional[T]:
		if self.__head is None:
			return None
		else:
			data : T = self.__head.data
			new_head : Optional[_Node[T]] = self.__head.prev
			if new_head is not None:
				new_head.next = None
			else:
				self.__tail = None
			self.__head = new_head
			return data
	
	def pop_back(self) -> Optional[T]:
		if self.__tail is None:
			return None
		else:
			data : T = self.__tail.data
			new_tail : Optional[_Node[T]] = self.__tail.next
			if new_tail is not None:
				new_tail.prev = None
			else:
				self.__head = None
			self.__tail = new_tail
			return data
	
	def append_front(self, other : Dequeue[T]) -> None:
		if self.__head is not None:
			if other.__tail is not None:
				self.__head.next = other.__tail
				other.__tail.prev = self.__head
				
				self.__head = other.__head
		else:
			if other.__tail is not None:
				self.__head = other.__head
				self.__tail = other.__tail
		
		other.__head = None
		other.__tail = None		
	
	def append_back(self, other : Dequeue[T]) -> None:
		if self.__tail is not None:
			if other.__head is not None:
				self.__tail.prev = other.__head
				other.__head.next = self.__tail
				
				self.__tail = other.__tail
		else:
			if other.__head is not None:
				self.__head = other.__head
				self.__tail = other.__tail
		
		other.__head = None
		other.__tail = None
	
	def convert_to_list(self) -> List[T]:
		ls : List[T] = []
		data : Optional[T] = self.pop_back()
		while data is not None:
			ls.append(data)
			data = self.pop_back()
		return ls
	
	def copy_to_list(self) -> List[T]:
		ls : List[T] = []
		current : Optional[_Node[T]] = self.__tail
		while current is not None:
			ls.append(current.data)
			current = current.next
		return ls

# TESTS

class TestEmpty(unittest.TestCase):
	def test_empty(self) -> None:
		dq : Dequeue[int] = Dequeue()
		self.assertTrue(dq.empty())

class TestSize(unittest.TestCase):
	def test_empty(self) -> None:
		dq : Dequeue[int] = Dequeue()
		self.assertEqual(dq.size(), 0)
	
	def test_size(self) -> None:
		dq : Dequeue[int] = Dequeue()
		dq.push_front(1)
		dq.push_back(0)
		self.assertEqual(dq.size(), 2)

class TestInsertion(unittest.TestCase):
	def __init__(self, *args, **kwargs) -> None:
		super(TestInsertion, self).__init__(*args, **kwargs)
		self.dequeue : Dequeue[int] = Dequeue()
		self.dequeue.push_front(0)
	
	def test_front(self) -> None:
		self.assertEqual(self.dequeue.front(), 0)
	
	def test_bask(self) -> None:
		self.assertEqual(self.dequeue.back(), 0)

class TestInsertionReuseAfterEmpty(unittest.TestCase):
	def __init__(self, *args, **kwargs) -> None:
		super(TestInsertionReuseAfterEmpty, self).__init__(*args, **kwargs)
		self.dequeue : Dequeue[int] = Dequeue()
		self.dequeue.push_front(0)
		self.dequeue.pop_front()
		self.dequeue.push_front(1)
	
	def test_front(self) -> None:
		self.assertEqual(self.dequeue.front(), 1)
	
	def test_back(self) -> None:
		self.assertEqual(self.dequeue.back(), 1)

class TestInsertionEptyingTwice(unittest.TestCase):
	def test_empty(self) -> None:
		dequeue : Dequeue[int] = Dequeue()
		dequeue.push_front(0)
		dequeue.pop_front()
		self.assertTrue(dequeue.empty())
		dequeue.push_front(1)
		dequeue.pop_front()
		self.assertTrue(dequeue.empty())

class TestInsertionEmptyingTwiceTwoSided(unittest.TestCase):
	def test_empty(self) -> None:
		dequeue : Dequeue[int] = Dequeue()
		dequeue.push_front(0)
		dequeue.pop_front()
		self.assertTrue(dequeue.empty())
		dequeue.push_front(1)
		dequeue.pop_back()
		self.assertTrue(dequeue.empty())

class TestInsertionTwice(unittest.TestCase):
	def __init__(self, *args, **kwargs) -> None:
		super(TestInsertionTwice, self).__init__(*args, **kwargs)
		self.dequeue : Dequeue[int] = Dequeue()
		self.dequeue.push_front(0)
		self.dequeue.push_back(1)
	
	def test_front(self) -> None:
		self.assertEqual(self.dequeue.front(), 0)
	
	def test_bask(self) -> None:
		self.assertEqual(self.dequeue.back(), 1)

class TestCopyToList(unittest.TestCase):
	def test_empty(self) -> None:
		dequeue : Dequeue[int] = Dequeue()
		self.assertEqual(dequeue.copy_to_list(), [])
	
	def test_content(self) -> None:
		dequeue : Dequeue[int] = Dequeue()
		dequeue.push_front(1)
		dequeue.push_back(0)
		
		ls : List[int] = dequeue.copy_to_list()
		self.assertEqual(ls, [0,1])
	
	def test_persistence(self) -> None:
		dequeue : Dequeue[int] = Dequeue()
		dequeue.push_front(0)
		dequeue.push_front(1)
		
		ls : List[int] = dequeue.copy_to_list()
		self.assertEqual(ls, [0,1])
		ls = dequeue.copy_to_list()
		self.assertEqual(ls, [0,1])

class TestConvertToList(unittest.TestCase):
	def test_empty(self) -> None:
		dequeue : Dequeue[int] = Dequeue()
		self.assertEqual(dequeue.convert_to_list(), [])
	
	def test_content(self) -> None:
		dequeue : Dequeue[int] = Dequeue()
		dequeue.push_front(1)
		dequeue.push_back(0)
		
		ls : List[int] = dequeue.convert_to_list()
		self.assertEqual(ls, [0,1])
	
	def test_persistence(self) -> None:
		dequeue : Dequeue[int] = Dequeue()
		dequeue.push_front(0)
		dequeue.push_front(1)
		
		ls : List[int] = dequeue.convert_to_list()
		self.assertEqual(ls, [0,1])
		ls = dequeue.convert_to_list()
		self.assertEqual(ls, [])

def main() -> None:
	unittest.main(exit = False)
	# To disable in interactive sessions:
	#import os, sys
	#if os.isatty(sys.stdout.fileno()):
	#	pass

if __name__ == '__main__':
	main()
