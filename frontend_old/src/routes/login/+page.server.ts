
import { post, browserGet, browserSet } from '$lib/utils/requestUtils';
import { variables } from '$lib/utils/constants';
import { notificationData } from '$lib/store/notificationStore';
import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */

export const load = async ({ cookies }) => {
  if (cookies.get('refreshToken')) {
    throw redirect(303, "/main");
  }
};
export const actions = {
  handleLogin: async ({ cookies, request }) => {
    const data = await request.formData();
    if (cookies.get('refreshToken')) {
      await cookies.delete('refreshToken');
    }
    const [jsonRes] = await post(fetch, `${variables.BASE_API_URI}/login/`, {
      user: {
        phone_number: data.get('phone_number'),
        password: data.get('password')
      }
    });
    const response: UserResponse = jsonRes;

    const err = jsonRes.user.error ? jsonRes.user.error : [];
    if (err.length > 0) {
      return { success: false, data: err };
    } else if (response.user) {
      if (response.user.tokens && response.user.tokens.refresh) {
        browserSet('refreshToken', response.user.tokens.refresh);
        cookies.set('refreshToken', `${response.user.tokens.refresh}`, {
          httpOnly: true,
          path: '/main',
          secure: true,
          sameSite: 'strict',
          maxAge: 60 * 60 * 24 // 1 day
        });
      }
      notificationData.update(() => 'Login successful...');
      throw redirect(301, '/main');
    }
  }
};