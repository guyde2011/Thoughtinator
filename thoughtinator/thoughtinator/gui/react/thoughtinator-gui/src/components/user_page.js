import React from 'react';
import FetchComponent from './fetch_component'
import * as api_defaults from '../api/defaults'
import { main_page } from './main_page';
import SnapshotPage from './snapshot_page'
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

function sameDates(date, date2) {
    return date2.getDate() == date.getDate() &&
            date2.getMonth() == date.getMonth() &&
            date2.getUTCFullYear() == date.getUTCFullYear()
}

class UserPage extends FetchComponent { 

    getInitialState() {
        return {date: null}
    }

    componentDidMount() {
        super.componentDidMount()
        let user_promise = this.api.getUser(this.props.user_id);
        this.bind('user', user_promise);
        this.bind('snapshots', user_promise.then(user => user.snapshots));
    }

    setDate = (date) => {
        if (this._mounted)
            this.setState({date: date})
    } 

    render () {
        return (
        <div id="user-panel">
            {this.bound(['user'], () => (  
                <div>                
                    <UserPanel user={this.fetched.user} onClick={this.onBack}></UserPanel>
                    {this.bound(['snapshots'], () => (
                    <div className="jumbotron" name="card-bg" style={{fontSize: 18, float: 'right', display: 'inline-block', marginTop: '6.25%', marginRight: '10%', width: '27.5%'}}>
                        <DatePicker
                        startDate={this.state.date}
                        onChange={this.setDate}
                        includeDates={this.fetched.snapshots.map(s => new Date(parseInt(s.datetime)))}
                        placeholderText="Select a date for the snapshots"
                        dateFormat="MMMM d, yyyy"
                        />
                    </div>))}
                    <SnapshotList user={this.fetched.user} date={this.state.date}/>
            </div>
            ))}

        </div>
        );
    }

    onBack = () => {
        main_page().swapUp()
    }
}

class UserPanel extends FetchComponent {


    render() {
        let user = this.props.user;
        return (
        <div className="jumbotron" name="card-bg" id='user-page' onClick={this.props.onClick}>
                <img src={api_defaults.GENDER_IMAGES[user.gender]} style={{display: 'inline-block', float: 'right', width: 128, height: 128}}></img>
                <b>Name</b> {user.username} <br/>
                <b>User Id</b> {user.user_id} <br/>
                <b>Birthday</b> {user.birthday.getDate()}/{user.birthday.getMonth()}/{user.birthday.getUTCFullYear()} <br/>
                <b>Age</b> {(new Date(Date.now() - user.birthday)).getUTCFullYear() - 1970} <br/>
        </div>
        )
    }
}

class SnapshotList extends FetchComponent { 

    componentDidMount() {
        super.componentDidMount()
        this.bind('snapshots', this.props.user.snapshots);
    }

    render () {
        if (this.props.date == null) {
            return (

            <div className='snapshots-list' style={{overflowX: 'scroll', whiteSpace: 'nowrap', maxHeight: 350, overflowY: 'hidden', width: '100%'}}>        
            <div>
                {this.bound(['snapshots'], () => this.fetched.snapshots.map(snap => 
                <div key={snap.snap_id} style={{display: 'inline-block', padding: '10px'}}>
                <SnapshotInfo user={this.props.user} snap_id={snap.snap_id} snap_date={snap.datetime} style={{width: 300, height: 300}}/>
                </div>
                ))}
            </div></div>
            );
        }
        return (

            <div className='snapshots-list' style={{overflowX: 'scroll', whiteSpace: 'nowrap', maxHeight: 350, overflowY: 'hidden', width: '100%'}}>        
            <div>
                {this.bound(['snapshots'], () => this.fetched.snapshots.filter(s => sameDates(new Date(parseInt(s.datetime)), this.props.date)).map(snap => 
                <div key={snap.snap_id} style={{display: 'inline-block', padding: '10px'}}>
                <SnapshotInfo user={this.props.user} snap_id={snap.snap_id} snap_date={snap.datetime} style={{width: 300, height: 300}}/>
                </div>
                ))}
            </div></div>
            );
    }
}

class SnapshotInfo extends FetchComponent {

    handleClick = () => {
        main_page().swapDown({page: SnapshotPage, props: {user: this.props.user, snap: this.props.snap_id}})
    }

    render() {
        return (
        <div id="snap-info" name="card-bg" onClick={this.handleClick} className="card" style={{width: 300, height: 300, display: 'inline-block', verticalAlign: 'text-top'}}>

            <div className="card-body" style={{fontSize: 18}}>
                <b>Snapshot ID</b><br/>{this.props.user.username}#{this.props.snap_id} <br/><br/>
                <b>Time</b><br/>{new Date(parseInt(this.props.snap_date)).toUTCString()} <br/>
            </div>

        </div>)
    }
}


export default UserPage;