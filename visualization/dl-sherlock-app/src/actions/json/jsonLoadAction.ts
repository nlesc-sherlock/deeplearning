import { JSON_LOAD_ACTION }    from '../authorized-actions';

export const jsonLoadAction = (d3JSON: any) => {
    return {
        type: JSON_LOAD_ACTION,
        payload: { d3JSON }
    };
};
