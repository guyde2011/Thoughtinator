import React from 'react';
import FetchComponent from './fetch_component'
import * as api_defaults from '../api/defaults'
import {main_page} from './main_page'
import UserPage from './user_page';
class UsersPage extends FetchComponent { 

    componentDidMount() {
        super.componentDidMount()
        this.bind('users', this.api.getUsers());
    }

    render () {
        return (
        <div>
            <div id='welcome-div'>
                <div id='welcome1'> Welcome to Thoughtinator-3000 </div>
                <div id='welcome2'> Please select a user </div>

            </div>
            <div id='welcome3'>     
            <div className='triangle-right'></div>
                                    Made by Doctor Heinz Doofenshmirtz <br/>
                                    using React to make accessing <br/>
                                    saved snapshots easier. <br/>
                                    Have a great <br/>
                                    time.</div>
        <div className='users-list' style={{overflowX: 'scroll', whiteSpace: 'nowrap', maxHeight: 350, overflowY: 'hidden', width: '100%'}}>        
        <div>
            {this.bound(['users'], () => this.fetched.users.map(user => 
            <div key={user.user_id} style={{display: 'inline-block', padding: '10px'}}>
            <UserInfo user_id={user.user_id} style={{width: 300, height: 300}}/>
            </div>
            ))}
        </div></div></div>
        );
    }
}

class UserInfo extends FetchComponent {
    componentDidMount() {
        super.componentDidMount()
        let user_promise = this.api.getUser(this.props.user_id);
        this.bind('user', user_promise);
        this.bind('color_image', user_promise
            .then(user => user?.snapshots)
            .then(snaps => snaps?.find(_ => true))
            .then(snap => user_promise.then(user => user?.getSnapshot(snap?.snap_id ?? -1)))
            .then(snap => snap?.colorImage ?? api_defaults.NO_COLOR_IMAGE));
    }

    handleClick = () => {
        main_page().swapDown({page: UserPage, props: {user_id: this.fetched.user.user_id, id: "user_page"}})
    }

    render() {
        return (
        <div name="card-bg" onClick={this.handleClick} className="card" style={{width: 300, height: 300, display: 'inline-block', verticalAlign: 'text-top'}}>
        {this.bound(['user'], () => ( <div>
                {this.bound(['color_image'], () => 
                    <img className="card-img-top" src={`${this.fetched.color_image}`} alt={this.fetched.user.username}></img>
                )}                
                {this.unbound(['color_image'], () => 
                    <img className="card-img-top" src={`${api_defaults.LOADING}`} alt={this.fetched.user.username}></img>
                )}
                <div className="card-body">
                    <img src={api_defaults.GENDER_IMAGES[this.fetched.user.gender]} style={{display: 'inline-block', float: 'right', width: 64, height: 64}}></img>
                    <b>Name</b> {this.fetched.user.username} <br/>
                    <b>User Id</b> {this.fetched.user.user_id} <br/>
                    <b>Birthday</b> {this.fetched.user.birthday.getDate()}/{this.fetched.user.birthday.getMonth()}/{this.fetched.user.birthday.getUTCFullYear()} <br/>
                    <b>Age</b> {(new Date(Date.now() - this.fetched.user.birthday)).getUTCFullYear() - 1970} <br/>
                </div>
            </div>
        ))}
        </div>)
    }
}

export default UsersPage;