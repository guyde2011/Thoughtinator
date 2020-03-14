class User {
    
    constructor(api, user_id, username, birthday, gender) {
        this.api = api;
        this.user_id = user_id;
        this.username = username;
        this.birthday = new Date(birthday * 1000);
        this.gender = gender
    }

    get snapshots() {
        let ret = this.api.getSnapshots(this.user_id);
        ret = ret.then(f => {this.getSnapshot(f.find(_ =>true).snap_id).then(x => x.colorImage).then(console.log); return f})
        return ret
    }

    getSnapshot(snap_id) {
        if (snap_id >= 0)
            return this.api.getSnapshot(this.user_id, snap_id)
    }
}
export default User;