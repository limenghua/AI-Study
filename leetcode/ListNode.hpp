#pragma once
#include <iostream>
#include <vector>
 //Definition for singly-linked list.
 struct ListNode {
     int val;
     ListNode *next;
     ListNode() : val(0), next(nullptr) {}
     ListNode(int x) : val(x), next(nullptr) {}
     ListNode(int x, ListNode *next) : val(x), next(next) {}
 };

 inline void printList(ListNode* head) {
     while (head) {
         std::cout << head->val << " ";
         head = head->next;
     }
     std::cout << std::endl;
 }

 inline ListNode* createList(std::vector<int>& arr) {
    if(arr.empty()) return nullptr;

    ListNode* dummy = new ListNode(arr[0]);
    ListNode* curr = dummy;
    for (int i = 1; i < arr.size(); i++) {
        curr->next = new ListNode(arr[i]);
        curr = curr->next;
    }
    return dummy;
 }


