import { JSON_LOAD_ACTION }      from '../actions';

import { GenericAction }  from '../types';

const initstate: any = {
    d3JSON: {}
};

export const imageChartReducer = (state: any = initstate, action: GenericAction) => {
    if (action.type === JSON_LOAD_ACTION) {
        const { d3JSON } = action.payload;
        return Object.assign({}, { d3JSON });
    } else {
        return state;
    }
};
