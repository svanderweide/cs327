#pragma once

#include <iostream>

template <class T>
class Node
{
    T data;
    Node<T>* next;

public:
    Node(T d) : data(d), next(nullptr) {}

    const T& get() const
    {
        return data;
    }

    Node<T>* getNext() const
    {
        return next;
    }

    void setNext(Node<T>* n)
    {
        next = n;
    }

    bool hasNext()
    {
        return next != nullptr;
    }
};

template <class T>
class LinkedListIterator
{
    Node<T>* current;

public:
    LinkedListIterator(Node<T>* n) : current(n) {}

    bool isDone() const
    {
        return current == nullptr;
    }
    T next()
    {
        T ret = current->get();
        current = current->getNext();
        return ret;
    }
};

template <class T>
class LinkedList
{
    Node<T>* head;

public:
    LinkedList() : head(nullptr) {}

    LinkedListIterator<T> getIter()
    {
        return LinkedListIterator<T>(head);
    }

    void push(T data)
    {
        Node<T>* newNode = new Node<T>(data);
        newNode->setNext(head);
        head = newNode;
    }

    T pop()
    {
        T ret = head->get();
        head = head->getNext();
        return ret;
    }
};