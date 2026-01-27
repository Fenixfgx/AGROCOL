/**
 * AGROCOL HS SAS - Language Switcher
 * Handles bilingual functionality (English/Spanish)
 * Default language: English
 */

(function($) {
    'use strict';
    
    // Configuration
    const STORAGE_KEY = 'agrocol_language';
    const DEFAULT_LANG = 'en';
    const AVAILABLE_LANGUAGES = ['en', 'es'];
    
    // Language switcher object
    const LanguageSwitcher = {
        
        /**
         * Initialize language switcher
         */
        init: function() {
            // Load saved language or use default
            const savedLang = this.getStoredLanguage();
            const initialLang = savedLang || DEFAULT_LANG;
            
            // Set initial language
            this.setLanguage(initialLang, false);
            
            // Update language selector dropdown
            this.updateSelector(initialLang);
            
            // Bind language selector change event
            this.bindSelectorEvent();
            
            console.log('Language Switcher initialized - Current language:', initialLang);
        },
        
        /**
         * Get stored language from localStorage
         */
        getStoredLanguage: function() {
            try {
                const stored = localStorage.getItem(STORAGE_KEY);
                if (stored && AVAILABLE_LANGUAGES.includes(stored)) {
                    return stored;
                }
            } catch (e) {
                console.warn('localStorage not available:', e);
            }
            return null;
        },
        
        /**
         * Store language preference
         */
        storeLanguage: function(lang) {
            try {
                localStorage.setItem(STORAGE_KEY, lang);
            } catch (e) {
                console.warn('Could not save language preference:', e);
            }
        },
        
        /**
         * Update language toggle switch
         */
        updateSelector: function(lang) {
            const $toggle = $('#language-toggle');
            const $flagImg = $('#flag-img');
            
            if ($toggle.length) {
                // Update toggle state (active = Spanish)
                if (lang === 'es') {
                    $toggle.addClass('active');
                    if ($flagImg.length) {
                        $flagImg.attr('src', 'assets/img/flag-colombia.svg');
                    }
                } else {
                    $toggle.removeClass('active');
                    if ($flagImg.length) {
                        $flagImg.attr('src', 'assets/img/flag-usa.svg');
                    }
                }
                
                console.log('Toggle updated to:', lang);
            }
        },
        
        /**
         * Bind change event to language toggle
         */
        bindSelectorEvent: function() {
            const self = this;
            
            // Handle toggle click
            $(document).on('click', '#language-toggle', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const $toggle = $(this);
                const isActive = $toggle.hasClass('active');
                
                // Toggle between languages
                const newLang = isActive ? 'en' : 'es';
                
                // Change language
                self.setLanguage(newLang, true);
                
                console.log('Language toggled to:', newLang);
            });
        },
        
        /**
         * Set active language and translate all elements
         */
        setLanguage: function(lang, saveToStorage) {
            // Validate language
            if (!AVAILABLE_LANGUAGES.includes(lang)) {
                console.warn('Invalid language:', lang);
                lang = DEFAULT_LANG;
            }
            
            // Store preference if requested
            if (saveToStorage) {
                this.storeLanguage(lang);
            }
            
            // Update HTML lang attribute
            $('html').attr('lang', lang);
            
            // Translate all elements with data-lang attribute
            this.translateElements(lang);
            
            // Update selector
            this.updateSelector(lang);
            
            // Trigger custom event
            $(document).trigger('languageChanged', [lang]);
            
            console.log('Language changed to:', lang);
        },
        
        /**
         * Translate all elements with data-lang attributes
         */
        translateElements: function(lang) {
            const self = this;
            
            // Check if translations object exists
            if (typeof translations === 'undefined') {
                console.error('Translations object not found. Make sure translations.js is loaded.');
                return;
            }
            
            // Get language translations
            const langTranslations = translations[lang];
            if (!langTranslations) {
                console.error('Translations not found for language:', lang);
                return;
            }
            
            // Find and translate all elements with data-lang attribute
            $('[data-lang]').each(function() {
                const $element = $(this);
                const key = $element.data('lang');
                
                if (!key) return;
                
                // Get translation using dot notation (e.g., "nav.home")
                const translation = self.getNestedTranslation(langTranslations, key);
                
                if (translation) {
                    // Check if element has special attribute to update
                    const updateAttr = $element.data('lang-attr');
                    
                    if (updateAttr) {
                        // Update specific attribute (e.g., placeholder, title)
                        $element.attr(updateAttr, translation);
                    } else {
                        // Update text content (handle HTML if needed)
                        if ($element.data('lang-html')) {
                            $element.html(translation);
                        } else {
                            $element.text(translation);
                        }
                    }
                } else {
                    console.warn('Translation not found for key:', key);
                }
            });
        },
        
        /**
         * Get nested object property using dot notation
         * Example: getNestedTranslation(obj, "nav.home") returns obj.nav.home
         */
        getNestedTranslation: function(obj, key) {
            return key.split('.').reduce(function(o, k) {
                return o && o[k] !== undefined ? o[k] : null;
            }, obj);
        },
        
        /**
         * Get current active language
         */
        getCurrentLanguage: function() {
            return $('html').attr('lang') || DEFAULT_LANG;
        },
        
        /**
         * Switch to specific language
         */
        switchTo: function(lang) {
            this.setLanguage(lang, true);
        }
    };
    
    // Initialize on document ready
    $(document).ready(function() {
        // Wait a bit for Nice Select to initialize
        setTimeout(function() {
            LanguageSwitcher.init();
        }, 100);
    });
    
    // Make it globally accessible
    window.LanguageSwitcher = LanguageSwitcher;
    
})(jQuery);
