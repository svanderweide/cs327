#pragma once

#include <cstddef>
#include <iostream>

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
    T * reference;
    ReferenceCounter * refcounter;

public:
    SmartPointer(T *pValue) : reference(pValue) {
        // initialize dumb pointer
        // set up and increment reference counter
        refcounter = new ReferenceCounter();
        refcounter->increment();
    }

    // Copy constructor
    SmartPointer(const SmartPointer<T> &sp) {
        // Copy the data and reference pointer
        // increment the reference count
        reference = sp.reference;
        refcounter = sp.refcounter;
        refcounter->increment();
    }

    // Destructor
    ~SmartPointer() {
        // Decrement the reference count
        // if reference become zero delete the data
        if (refcounter)
        {
            if (refcounter->decrement() < 1)
            {
                delete reference;
                reference = nullptr;
                delete refcounter;
                refcounter = nullptr;
            }
        }
    }

    T& operator*() {
        // delegate
        return *reference;
    }

    T* operator->() {
        // delegate
        return reference;
    }

    // Assignment operator
    SmartPointer<T> &operator=(const SmartPointer<T> &sp)
    {
        // Deal with old SmartPointer that is being overwritten
        // Copy sp into this (similar to copy constructor)
        // return this
        if (refcounter)
        {
            if (refcounter->decrement() < 1)
            {
                delete reference;
                reference = nullptr;
                delete refcounter;
                refcounter = nullptr;
            }
        }

        if (!(sp == nullptr))
        {
            reference = sp.reference;
            refcounter = sp.refcounter;
            refcounter->increment();
        }

        SmartPointer<T>& ref_sp = *this;
        return ref_sp;
    }

    // Check equal to nullptr
    bool operator==(std::nullptr_t rhs) const
    {
        return (reference == rhs);
    }
};
