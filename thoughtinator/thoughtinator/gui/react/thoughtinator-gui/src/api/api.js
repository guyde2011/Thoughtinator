import User from './user';
import Snapshot from './snapshot'
class API {
    constructor(host, port) {
        this.host = host;
        this.port = port;
        this.cache = {};
    }

    get url() {
        return `${this.host}:${this.port}`;
    }

    getSubpath(subpath) {
        if (subpath in this.cache) {
            return new Promise((resolve, reject) => resolve(this.cache[subpath]))
        }
        return fetch(`http://${this.url}/${subpath}`, 
            {method: 'GET', mode: 'cors', dataType: 'json'})
            .then(r => r.headers.get('content-type').indexOf('application/json') != -1 ? r.json() : undefined)
            .then(r => {this.cache[subpath] = r; return r});
    }

    getUsers() {
        return this.getSubpath('users');
    }

    getUser(user_id) {
        let fields = ['user_id', 'username', 'birthday', 'gender'];
        return this.getSubpath(`users/${user_id}`)
            .then(user => fields.map(f => user?.[f]))
            .then(fields => fields.includes(undefined) ? undefined : new User(this, ...fields));
    }

    getSnapshots(user_id) {
        return this.getSubpath(`users/${user_id}/snapshots`);
    }

    getSnapshot(user_id, snap_id){
        let fields = ['snap_id', 'datetime', 'fields']
        return this.getSubpath(`users/${user_id}/snapshots/${snap_id}`)            
            .then(snap => fields.map(f => snap[f]))
            .then(fields => new Snapshot(this, user_id, ...fields));
    }

    getField(user_id, snap_id, field) {
        return this.getSubpath(`users/${user_id}/snapshots/${snap_id}/${field}`);
    }

    getDataURL(user_id, snap_id, field) {
        return `http://${this.url}/users/${user_id}/snapshots/${snap_id}/${field}/data`;
    }
}

export default API;