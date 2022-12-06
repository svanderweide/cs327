#pragma once

#include <iostream>
#include "SmartPointer.hpp"

template <class T>
class Node
{
    T data;
    SmartPointer<Node<T>> next;

public:
    Node(T d) : data(d), next(nullptr) {}

    const T& get() const
    {
        return data;
    }

    SmartPointer<Node<T>> getNext() const
    {
        return next;
    }

    void setNext(SmartPointer<Node<T>> n)
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
    SmartPointer<Node<T>> current;

public:
    LinkedListIterator(SmartPointer<Node<T>> n) : current(n) {}

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
    SmartPointer<Node<T>> head;

public:
    LinkedList() : head(nullptr) {}

    ~LinkedList()
    {
        SmartPointer<Node<T>> tmpNode = nullptr;
        while (!(head->getNext() == nullptr))
        {
            tmpNode = head;
            head = head->getNext();
            tmpNode->setNext(nullptr);
        }
    }

    LinkedListIterator<T> getIter()
    {
        return LinkedListIterator<T>(head);
    }

    void push(T data)
    {
        SmartPointer<Node<T>> newNode = new Node<T>(data);
        newNode->setNext(head);
        head = newNode;
    }

    T pop()
    {
        SmartPointer<Node<T>> tmpNode = head;
        head = head->getNext();
        tmpNode->setNext(nullptr);
        return tmpNode->get();
    }
};
