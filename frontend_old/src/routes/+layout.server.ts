import { notificationData } from '$lib/store/notificationStore';

export const load = async ({ locals }) => {
    
    if(locals.user){
        notificationData.set('');
        return {user: {status: true, data: {id: locals.user.id, phone_number: locals.user.phone_number, refreshToken: locals.user.tokens.refresh}}}
    }else{
        return {user: {status: false}}
    }
}

