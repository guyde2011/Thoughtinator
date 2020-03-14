
class Snapshot {
    constructor(api, user_id, snap_id, datetime, fields) {
        this.api = api;
        this.user_id = user_id;
        this.snap_id = snap_id;
        this.datetime = new Date(parseInt(datetime));
        this.fields = fields;
    }

    get user() {
        return this.api.getUser(this.user_id);
    }

    get colorImage() {
        if (this.fields.includes('color_image')) 
            return this.api.getDataURL(this.user_id, this.snap_id, 'color-image');
        return '/static/missing_color_image.png';
    }

    get depthImage() {
        if (this.fields.includes('depth_image')) 
            return this.api.getDataURL(this.user_id, this.snap_id, 'depth-image');
        return '/static/missing_depth_image.png';
    }

    get feelings() {
        if (this.fields.includes('feelings')) 
            return this.api.getField(this.user_id, this.snap_id, 'feelings');
        return null;
    }
    
    get pose() {
        if (this.fields.includes('pose')) 
            return this.api.getField(this.user_id, this.snap_id, 'pose');
        return null;
    }
}

export default Snapshot;