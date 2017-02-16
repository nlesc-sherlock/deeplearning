import { exampleReducer }                         from './';
import { imageChartReducer }                      from './';

import { GenericAction }              from '../types';

const overallInitstate: any = {};

/* Function needed to give only _part_ of the state to the individual trees, 
    but the _whole_ state to the queryReducer     
*/
export const combinedReducer = (state: any = overallInitstate, action: GenericAction) => {
    const result : any = {};
    console.log(new Date().toISOString().slice(11, 19), action.type);

    //These reducers need the whole state
    result.example = exampleReducer(state.example, action);
    result.imageChart = imageChartReducer(state.imageChart, action);

    return result;
};
