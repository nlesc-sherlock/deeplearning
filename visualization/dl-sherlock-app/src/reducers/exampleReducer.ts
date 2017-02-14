import { EXAMPLE_ACTION }      from '../actions';

import { GenericAction }  from '../types';

const initstate: any = {
    imageSrc: ''
};

export const exampleReducer = (state: any = initstate, action: GenericAction) => {
    if (action.type === EXAMPLE_ACTION) {
        const { imageSrc } = action.payload;
        return Object.assign({}, { imageSrc });
    } else {
        return state;
    }
};
