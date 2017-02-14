import { applyMiddleware }        from 'redux';
import { createStore }            from 'redux';
import thunk                      from 'redux-thunk';

import { exampleReducer }         from './reducers';

import { exampleThunk }           from './actions';

export const store = createStore(exampleReducer, applyMiddleware(thunk));

// whenever the store has changed, print the new state
store.subscribe(() => {
    // eslint-disable-next-line
    console.log(store.getState());
});

store.dispatch(exampleThunk('../images/exampleImage.jpg'));
