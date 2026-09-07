/**
 * nv analytics — Supabase Auth Client Module
 * Handles client initialization, session persistence, authentication flows,
 * and dynamic credential resolution from backend /api/auth/config or localStorage.
 */

(function (window) {
  const STORAGE_KEY_URL = 'nv_supabase_url';
  const STORAGE_KEY_KEY = 'nv_supabase_anon_key';

  let supabaseClient = null;
  let authListeners = [];

  const SupabaseAuth = {
    /**
     * Retrieve current configuration from localStorage or backend API
     */
    async getConfig() {
      const localUrl = localStorage.getItem(STORAGE_KEY_URL);
      const localKey = localStorage.getItem(STORAGE_KEY_KEY);

      if (localUrl && localKey) {
        return { url: localUrl, key: localKey, source: 'localStorage' };
      }

      try {
        const res = await fetch('/api/auth/config');
        if (res.ok) {
          const data = await res.json();
          if (data.supabase_url && data.supabase_anon_key) {
            return {
              url: data.supabase_url,
              key: data.supabase_anon_key,
              source: 'backend'
            };
          }
        }
      } catch (err) {
        console.warn('[SupabaseAuth] Could not fetch auth config from backend:', err);
      }

      return {
        url: localUrl || '',
        key: localKey || '',
        source: 'none'
      };
    },

    /**
     * Set configuration in localStorage and re-initialize client
     */
    setConfig(url, key) {
      if (url) localStorage.setItem(STORAGE_KEY_URL, url.trim());
      else localStorage.removeItem(STORAGE_KEY_URL);

      if (key) localStorage.setItem(STORAGE_KEY_KEY, key.trim());
      else localStorage.removeItem(STORAGE_KEY_KEY);

      supabaseClient = null;
      return this.getClient();
    },

    /**
     * Clear custom local configuration
     */
    clearConfig() {
      localStorage.removeItem(STORAGE_KEY_URL);
      localStorage.removeItem(STORAGE_KEY_KEY);
      supabaseClient = null;
    },

    /**
     * Initialize or return existing Supabase client instance
     */
    async getClient() {
      if (supabaseClient) return supabaseClient;

      if (!window.supabase) {
        console.error('[SupabaseAuth] Supabase JS library (@supabase/supabase-js) is not loaded on window.');
        return null;
      }

      const config = await this.getConfig();
      if (!config.url || !config.key || config.url.includes('your-project') || config.key.includes('your-anon-key')) {
        console.warn('[SupabaseAuth] Supabase URL or Anon Key is missing or default placeholder.');
        return null;
      }

      try {
        supabaseClient = window.supabase.createClient(config.url, config.key, {
          auth: {
            persistSession: true,
            autoRefreshToken: true,
            detectSessionInUrl: true,
            storage: window.localStorage
          }
        });

        // Set up global listener
        supabaseClient.auth.onAuthStateChange((event, session) => {
          authListeners.forEach(cb => {
            try { cb(event, session); } catch (e) { console.error(e); }
          });
        });

        return supabaseClient;
      } catch (err) {
        console.error('[SupabaseAuth] Initialization error:', err);
        return null;
      }
    },

    /**
     * Subscribe to auth state changes
     */
    onAuthStateChange(callback) {
      authListeners.push(callback);
      // Immediately invoke with current session if available
      this.getSession().then(session => {
        if (session) {
          callback('INITIAL_SESSION', session);
        }
      });
      return () => {
        authListeners = authListeners.filter(cb => cb !== callback);
      };
    },

    /**
     * Get current active session
     */
    async getSession() {
      const client = await this.getClient();
      if (!client) return null;
      try {
        const { data, error } = await client.auth.getSession();
        if (error) throw error;
        return data?.session || null;
      } catch (err) {
        console.warn('[SupabaseAuth] getSession failed:', err);
        return null;
      }
    },

    /**
     * Get current logged-in user
     */
    async getUser() {
      const session = await this.getSession();
      return session?.user || null;
    },

    /**
     * Sign in with Email and Password
     */
    async signInWithEmail(email, password) {
      const client = await this.getClient();
      if (!client) {
        throw new Error('Supabase is not configured. Please configure your Project URL and Anon Key.');
      }
      const { data, error } = await client.auth.signInWithPassword({
        email: email.trim(),
        password: password
      });
      if (error) throw error;
      return data;
    },

    /**
     * Sign up with Email, Password and optional user metadata
     */
    async signUpWithEmail(email, password, metadata = {}) {
      const client = await this.getClient();
      if (!client) {
        throw new Error('Supabase is not configured. Please configure your Project URL and Anon Key.');
      }
      const { data, error } = await client.auth.signUp({
        email: email.trim(),
        password: password,
        options: {
          data: metadata
        }
      });
      if (error) throw error;
      return data;
    },

    /**
     * Send Magic Link / Passwordless login email
     */
    async sendMagicLink(email, redirectTo = window.location.origin) {
      const client = await this.getClient();
      if (!client) {
        throw new Error('Supabase is not configured. Please configure your Project URL and Anon Key.');
      }
      const { data, error } = await client.auth.signInWithOtp({
        email: email.trim(),
        options: {
          emailRedirectTo: redirectTo
        }
      });
      if (error) throw error;
      return data;
    },

    /**
     * Send Password Reset Email
     */
    async sendPasswordReset(email, redirectTo = `${window.location.origin}/login`) {
      const client = await this.getClient();
      if (!client) {
        throw new Error('Supabase is not configured. Please configure your Project URL and Anon Key.');
      }
      const { data, error } = await client.auth.resetPasswordForEmail(email.trim(), {
        redirectTo: redirectTo
      });
      if (error) throw error;
      return data;
    },

    /**
     * Sign in with OAuth Provider (google, github, etc.)
     */
    async signInWithOAuth(provider, redirectTo = window.location.origin) {
      const client = await this.getClient();
      if (!client) {
        throw new Error('Supabase is not configured. Please configure your Project URL and Anon Key.');
      }
      const { data, error } = await client.auth.signInWithOAuth({
        provider: provider,
        options: {
          redirectTo: redirectTo
        }
      });
      if (error) throw error;
      return data;
    },

    /**
     * Sign Out
     */
    async signOut() {
      const client = await this.getClient();
      if (client) {
        try {
          await client.auth.signOut();
        } catch (err) {
          console.warn('[SupabaseAuth] signOut warning:', err);
        }
      }
      // Notify listeners
      authListeners.forEach(cb => {
        try { cb('SIGNED_OUT', null); } catch (e) { console.error(e); }
      });
    }
  };

  window.SupabaseAuth = SupabaseAuth;
})(window);
