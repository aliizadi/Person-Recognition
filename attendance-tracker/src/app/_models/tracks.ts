import {Person} from './persons'
import {Camera} from './cameras'

export class Tracks {
    tracks: Track[];
}

export class Track {
    id: string;
    encoding_id: string;
    person: Person;
    date: string;
    time: string;
    kind: string;
    camera: Camera;
    image: string;
}
