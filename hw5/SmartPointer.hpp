#pragma once

#include <cstddef>

class ReferenceCounter
{
    int count; // Reference count
public:
    void increment() {
        count++;
    }
    int decrement() {
        return --count;
    }
};

template <typename T>
class SmartPointer
{
    // private instance variables for dumb pointer and ReferenceCounter

public:
    SmartPointer(T *pValue) {
        // initialize dumb pointer
        // set up and increment reference counter
    }

    // Copy constructor
    SmartPointer(const SmartPointer<T> &sp) {
        // Copy the data and reference pointer
        // increment the reference count
    }

    // Destructor
    ~SmartPointer() {
        // Decrement the reference count
        // if reference become zero delete the data
    }

    T& operator*() {
        // delegate
    }

    T* operator->() {
        // delegate
    }

    // Assignment operator
    SmartPointer<T> &operator=(const SmartPointer<T> &sp)
    {
        // Deal with old SmartPointer that is being overwritten

        // Copy sp into this (similar to copy constructor)

        // return this
    }

    // Check equal to nullptr
    bool operator==(std::nullptr_t rhs) const
    {
        
    }
};