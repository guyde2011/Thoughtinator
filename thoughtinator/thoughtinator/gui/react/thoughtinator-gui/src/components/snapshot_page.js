import React from 'react';
import FetchComponent from './fetch_component'
import * as api_defaults from '../api/defaults'
import { main_page } from './main_page';

class SnapshotPage extends FetchComponent { 
    componentDidMount(){
        super.componentDidMount()
        console.log(this.props)
        let snap_promise = this.props.user.getSnapshot(this.props.snap);
        this.bind('snapshot', snap_promise);

        this.bind('feelings', snap_promise
            .then(snap => snap.feelings));

        this.bind('pose', snap_promise
            .then(snap => snap.pose));

        this.bind('color_image', snap_promise
            .then(snap => snap.colorImage));

        this.bind('depth_image', snap_promise
            .then(snap => snap.depthImage));
        this.bind('prev_snapshot', this.props.user.snapshots
            .then(s => Math.max(...s.filter(x => x.snap_id < this.props.snap).map(x => x.snap_id))));
        this.bind('next_snapshot', this.props.user.snapshots
            .then(s => Math.min(...s.filter(x => x.snap_id > this.props.snap).map(x => x.snap_id))));

    }

    onBack = () => {
        main_page().swapUp()
    }

    onPrev = () => {
        let disabled=this.bound(['prev_snapshot'],
                () => this.fetched.prev_snapshot === -Infinity || this.fetched.prev_snapshot === NaN, () => true)
        if (!disabled)
            main_page().swapRight({page: SnapshotPage, props: {user: this.props.user, snap: this.fetched.prev_snapshot}})
    }

    onNext = () => {
        let disabled=this.bound(['next_snapshot'],
                () => this.fetched.next_snapshot === Infinity || this.fetched.next_snapshot === NaN, () => true)
        if (!disabled)
            main_page().swapLeft({page: SnapshotPage, props: {user: this.props.user, snap: this.fetched.next_snapshot}})
    }
    
    render(){
        let main_panel = <div id='main-snapshot-panel' name='card-bg'>
            <div className='title-panel'>Snapshot</div>
            <b>User</b> {this.props.user.username}#{this.props.user.user_id} <br/>
            <b>Snapshot ID</b> {this.props.snap} <br/>
            {this.bound(['snapshot'], () => <div><b>Date</b> {this.fetched.snapshot.datetime.toUTCString()} <br/></div>)}
        </div>
        let color_image = 
        <ImagePanel src={this.bound(['color_image'], 
            () => this.fetched.color_image, 
            () => api_defaults.LOADING)}
        alt="Color Image" title="Image"/>
        let depth_image = 
        <ImagePanel src={this.bound(['depth_image'], 
            () => this.fetched.depth_image, 
            () => api_defaults.LOADING)}
        alt="Depth Image" title="Depth Image"/>
        let pose = this.bound(['pose'], () => <PosePanel pose={this.fetched.pose}/>, () => <div></div>)
        let feelings = this.bound(['feelings'], () => <FeelingsPanel feelings={this.fetched.feelings}/>, () => <div></div>)
        let prev = <div id='prev-snap' name='card-bg' onClick={this.onPrev} disabled={this.bound(['prev_snapshot'],
        () => this.fetched.prev_snapshot === -Infinity || this.fetched.prev_snapshot === NaN, () => true)}>{"<"}</div>
        let next = <div id='next-snap' name='card-bg' onClick={this.onNext} disabled={this.bound(['next_snapshot'],
                    () => this.fetched.next_snapshot === Infinity || this.fetched.next_snapshot === NaN, () => true)}>{">"}</div>
        return (
            <div style={{color: 0xffffff}}>
                id: {this.props.snap}
                {next}{prev}
                <div className='column' id='images-div'>
                    <div>
                        {color_image}{pose}
                    </div>
                    <div id='a-block'>
                        {depth_image}
                        <div id='b-block'>
                            {feelings}
                            {main_panel}
                        </div>
                    </div>
                </div>
                <div className='column'/>
                <div id='back-snapshot' name='card-bg' onClick={this.onBack}>Back</div>
            </div>
        )
    }
}

class ImagePanel extends React.Component {
    render() {
        return (
            <div id='snap-image-panel' name="card-bg">
                <div style={{top: '10px', fontSize: '200%', textAlign: 'center'}}>
                    {this.props.title}
                </div>
                <img src={this.props.src} alt={this.props.alt} style={{width: '100%', borderBottomLeftRadius: '2%', borderBottomRightRadius: '2%'}}/>
                
            </div>
        )
    }
}

class PosePanel extends React.Component {
    render() {
        return (
            <div id='snap-pose-panel' name='card-bg'>
                <div class='title-panel' style={{top: '10px', fontSize: '200%', textAlign: 'center'}}>
                    Position
                </div>
                <div id="translation-div">
                    <b>Translation</b><br/>
                    <b>x</b> {this.props.pose.translation.x} <br/>
                    <b>y</b> {this.props.pose.translation.y} <br/>
                    <b>z</b> {this.props.pose.translation.z} <br/> 
                </div>
                <div id="rotation-div">
                    <b>Rotation</b><br/>
                    <b>x</b> {this.props.pose.rotation.x} <br/>
                    <b>y</b> {this.props.pose.rotation.y} <br/>
                    <b>z</b> {this.props.pose.rotation.z} <br/>
                    <b>w</b> {this.props.pose.rotation.w} <br/>
                </div>
            </div>
        )
    }
}
class FeelingsPanel extends React.Component {
    render() {
        return (
            <div id='snap-feelings-panel' name='card-bg'>
                <div class='title-panel' style={{top: '10px', fontSize: '200%', textAlign: 'center'}}>
                    Feelings
                </div>
                <div id='feelings-div'>
                {Object.keys(this.props.feelings).map(x => <div><b>{x}</b><br/> {this.props.feelings[x]} <br/></div>)}
                </div>
            </div>
        )
    }
}
export default SnapshotPage;