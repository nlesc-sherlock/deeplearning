import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { Cell, Grid }       from 'react-mdl';
import { Provider }         from 'react-redux';

import { ExampleComponent } from './components';
import { store }            from './store';

import './index.css';

ReactDOM.render(
  <Provider store={ store }>
    <Grid>
      <Cell col={ 4 }>
        <ExampleComponent />
      </Cell>
      <Cell col={ 4 } />
      <Cell col={ 4 } />
    </Grid>
  </Provider>,
  document.getElementById('root')
);
