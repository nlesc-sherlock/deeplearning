import { applyMiddleware }        from 'redux';
import { createStore }            from 'redux';
import thunk                      from 'redux-thunk';

import { combinedReducer }         from './reducers';

import { jsonLoadThunk }          from './actions';

export const store = createStore(combinedReducer, applyMiddleware(thunk));

// whenever the store has changed, print the new state
store.subscribe(() => {
    // eslint-disable-next-line
    console.log(store.getState());
});

store.dispatch(jsonLoadThunk('https://raw.githubusercontent.com/nlesc-sherlock/deeplearning/master/JSON/example-output/output_vis_demo.json'));
