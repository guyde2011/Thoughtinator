import React from 'react';
import FetchComponent from './fetch_component'
import UsersPage from './users_page'
import * as api_defaults from '../api/defaults'
var main_page = () => {}
class MainPage extends FetchComponent { 

    constructor(props) {
        super(props);
        this.lastPage = <div></div>//{page: UsersPage, props: {}};
        this.lastPages = []
        this.curPage = React.createElement(UsersPage, {})
        this.state = {move: 0, counter: 0}
        main_page = () => this
    }

    disableMove() {
        setTimeout(() => this.setState({move: 0}), 3100)
    }

    swapUp() {
        this.lastPage = this.curPage
        this.curPage = this.lastPages.pop();
        this.setState({move: 1, counter: this.state.counter + 1});
        this.disableMove()
    }

    swapDown(page) {   
        page = React.createElement(page.page, page.props) 
        this.lastPages.push(this.curPage)   
        this.lastPage = this.curPage;
        this.curPage = page;
        this.setState({move: -1, counter: this.state.counter + 1});
        this.disableMove()
    }
    swapLeft(page) {
        page = React.createElement(page.page, page.props) 
        this.lastPage = this.curPage
        this.curPage = page;
        this.setState({move: 2, counter: this.state.counter + 1});
        this.disableMove()
    }

    swapRight(page) {
        page = React.createElement(page.page, page.props) 
        this.lastPage = this.curPage;
        this.curPage = page;
        this.setState({move: -2, counter: this.state.counter + 1});
        this.disableMove()
    }

    render () {
        var last = this.lastPage
        var cur = this.curPage
        let move = this.state.move
        if (move === 0 || last === null) {
            return (<div style={{width: '100%', height: '100%', overflow: 'hidden'}}>
                {cur}
            </div>)
        }
        //last = React.createElement(last.page, last.props)
        //cur = React.createElement(cur.page, cur.props)
        if (move === 1) {
            return (
            <div style={{width: '100%', height: '100%', overflow: 'hidden'}}>
                <div className='last-page-up'>{last}</div>
                <div className='cur-page-up'>{cur}</div>
            </div>
            )
        } else if (move === -1) {
            return (
                <div style={{width: '100%', height: '100%', overflow: 'hidden'}}>
                    <div className='cur-page-down'>{cur} </div>
                    <div className='last-page-down'>{last}</div>
                </div>
            )
        } else if (move === 2) {
            return (
                <div style={{width: '100%', height: '100%', overflow: 'hidden'}}>
                    <div className='last-page-left'>{last} </div>
                    <div className='cur-page-left'>{cur}</div>
                </div>
            )
        } else if (move === -2) {
            return (
                <div style={{width: '100%', height: '100%', overflow: 'hidden'}}>
                    <div className='cur-page-right'>{cur} </div>
                    <div className='last-page-right'>{last}</div>
                </div>
            )
        } else {
            return <div>Looks like someone messed with the website :) (move={move})</div>
        }
        
    }
        
    
}

export {main_page};
export default MainPage;