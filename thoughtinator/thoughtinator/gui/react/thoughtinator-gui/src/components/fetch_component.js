import React from 'react';
import { api } from '../App';

class FetchComponent extends React.Component {
    constructor(props) {
        super(props);   
        this.state = { fetched: {} };
        this.fetched = {};
        this.api = api;
        this._mounted = false;
    }

    componentDidMount() { 
        this._mounted = true;
    }
    componentWillMount() { 
        this._mounted = false;
    }

    setFetched(key, value) {
        if (this._mounted && value !== undefined) {
            this.fetched[key] = value
            this.setState({ fetched: this.state.fetched + key });
        }
    }

    bound(keys, func = undefined, fallback = () => undefined) {
        if (func === undefined)
            func = () => this.fetched[keys[0]];
        if (keys.every(key => key in this.fetched)) {
            return func();
        }
        return fallback();
    }
    
    unbound(keys, func) {
        if (!keys.every(key => key in this.fetched)) {
            return func();
        }
    }

    bind(key, promise) {
        return promise.then(res => {this.setFetched(key, res); return res });
    }


}

export default FetchComponent;