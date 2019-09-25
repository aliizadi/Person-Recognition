import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-tracker',
  templateUrl: './tracker.component.html',
  styleUrls: ['./tracker.component.css']
})
export class TrackerComponent implements OnInit {

  elements: any = [
    {id: 1, first: 'Mark', last: 'Otto', time: '1398/6/31 8:30:00'},
    {id: 2, first: 'Jacob', last: 'Thornton', time: '1398/6/31 9:30:00'},
    {id: 3, first: 'Larry', last: 'the Bird', time: '1398/6/31 10:00:00'},
    {id: 4, first: 'Mark', last: 'Otto', time: '1398/6/31 8:30:00'},
    {id: 5, first: 'Jacob', last: 'Thornton', time: '1398/6/31 9:30:00'},
    {id: 6, first: 'Larry', last: 'the Bird', time: '1398/6/31 10:00:00'},
    {id: 7, first: 'Mark', last: 'Otto', time: '1398/6/31 8:30:00'},
    {id: 8, first: 'Jacob', last: 'Thornton', time: '1398/6/31 9:30:00'},
    {id: 9, first: 'Larry', last: 'the Bird', time: '1398/6/31 10:00:00'},
    {id: 10, first: 'Mark', last: 'Otto', time: '1398/6/31 8:30:00'},
    {id: 11, first: 'Jacob', last: 'Thornton', time: '1398/6/31 9:30:00'},
    {id: 12, first: 'Larry', last: 'the Bird', time: '1398/6/31 10:00:00'},
  ];

  headElements = ['ID', 'First Name', 'Last Name', 'Time'];

  constructor() { }

  ngOnInit() {
  }

}
