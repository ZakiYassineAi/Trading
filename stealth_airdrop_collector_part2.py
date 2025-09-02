# ═══════════════════════════════════════════════════════════════════════════════════════
# 🔍 SUPREME CONTENT EXTRACTION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════════════

class SupremeContentExtractor:
    """Advanced multi-strategy content extraction engine"""
    
    def __init__(self, scraper: SupremeStealthScraper):
        self.scraper = scraper
        self.ml_analyzer = AdvancedMLIntelligence()
        self.extraction_cache = {}
        self.performance_stats = {
            'extractions': 0, 'successful': 0, 'failed': 0,
            'cached_hits': 0, 'avg_processing_time': 0
        }
    
    async def extract_from_all_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Asynchronously extract from all sources with intelligent batching"""
        logger.info(f"🔍 Starting intelligence extraction from {len(sources)} sources...")
        
        all_results = []
        batch_size = CONFIG.MAX_CONCURRENT_REQUESTS
        
        # Process sources in batches
        for i in range(0, len(sources), batch_size):
            batch = sources[i:i + batch_size]
            logger.info(f"📦 Processing batch {i//batch_size + 1}/{(len(sources)-1)//batch_size + 1}")
            
            batch_results = await self._process_source_batch(batch)
            all_results.extend(batch_results)
            
            # Brief pause between batches
            if i + batch_size < len(sources):
                await asyncio.sleep(random.uniform(2, 5))
        
        # Apply advanced filtering and deduplication
        filtered_results = self._apply_advanced_filtering(all_results)
        
        logger.success(f"✅ Extracted {len(filtered_results)} high-quality items from {len(sources)} sources")
        return filtered_results
    
    async def _process_source_batch(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of sources concurrently"""
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=CONFIG.REQUEST_TIMEOUT),
            connector=aiohttp.TCPConnector(limit=CONFIG.MAX_CONCURRENT_REQUESTS)
        ) as session:
            
            tasks = []
            for source in sources:
                task = self._extract_from_source_async(source, session)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle exceptions
            valid_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"❌ Source {sources[i]['name']} failed: {result}")
                    self.performance_stats['failed'] += 1
                else:
                    valid_results.extend(result)
                    self.performance_stats['successful'] += 1
            
            return valid_results
    
    async def _extract_from_source_async(self, source: Dict[str, Any], 
                                       session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Extract from a single source asynchronously"""
        start_time = time.time()
        source_name = source['name']
        source_type = source.get('type', 'html')
        
        # Check cache first
        cache_key = f"{source_name}_{hash(str(source))}"
        if cache_key in self.extraction_cache:
            cache_time, cached_results = self.extraction_cache[cache_key]
            if time.time() - cache_time < CONFIG.CACHE_EXPIRY_HOURS * 3600:
                self.performance_stats['cached_hits'] += 1
                return cached_results
        
        results = []
        
        try:
            for endpoint in source['endpoints']:
                try:
                    if source_type == 'json_api':
                        extracted = await self._extract_from_api_async(endpoint, source, session)
                    elif source_type == 'rss':
                        extracted = await self._extract_from_rss_async(endpoint, source)
                    else:
                        extracted = await self._extract_from_html_async(endpoint, source, session)
                    
                    results.extend(extracted)
                    
                    # Rate limiting between endpoints
                    await asyncio.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    logger.debug(f"⚠️ Endpoint {endpoint} failed: {e}")
                    continue
            
            # Cache successful results
            self.extraction_cache[cache_key] = (time.time(), results)
            
            # Update performance stats
            processing_time = time.time() - start_time
            self.performance_stats['extractions'] += 1
            self.performance_stats['avg_processing_time'] = (
                (self.performance_stats['avg_processing_time'] * (self.performance_stats['extractions'] - 1) + processing_time) /
                self.performance_stats['extractions']
            )
            
            logger.info(f"📦 {source_name}: {len(results)} items extracted in {processing_time:.2f}s")
            
        except Exception as e:
            logger.error(f"💥 Source extraction failed for {source_name}: {e}")
        
        return results
    
    async def _extract_from_html_async(self, url: str, source: Dict[str, Any], 
                                     session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Extract from HTML sources with advanced parsing"""
        response_data = await self.scraper.async_stealth_get(url, session)
        
        if not response_data or response_data['status'] != 200:
            return []
        
        try:
            soup = BeautifulSoup(response_data['content'], 'lxml')
            results = []
            
            # Try configured selectors first
            selectors = source.get('selectors', {})
            if selectors:
                results = self._extract_with_advanced_selectors(soup, selectors, source, url)
            
            # Fallback: intelligent content discovery
            if not results:
                results = self._intelligent_content_discovery(soup, source, url)
            
            # Apply source-specific post-processing
            results = self._apply_source_specific_processing(results, source)
            
            return results
            
        except Exception as e:
            logger.debug(f"⚠️ HTML parsing failed for {url}: {e}")
            return []
    
    def _extract_with_advanced_selectors(self, soup: BeautifulSoup, selectors: Dict[str, str], 
                                       source: Dict[str, Any], url: str) -> List[Dict[str, Any]]:
        """Advanced extraction using CSS selectors with fallbacks"""
        containers = soup.select(selectors.get('container', 'article, .post, .card'))[:30]
        results = []
        
        for container in containers:
            try:
                # Multi-strategy title extraction
                title = self._extract_title_advanced(container, selectors)
                if not title or len(title) < 8:
                    continue
                
                # Advanced description extraction
                description = self._extract_description_advanced(container, selectors)
                
                # Smart URL extraction
                item_url = self._extract_url_advanced(container, url)
                
                # Content quality validation
                if self._validate_content_quality(title, description):
                    results.append({
                        'title': title[:300],  # Truncate very long titles
                        'description': description[:800],
                        'url': item_url,
                        'source': source['name'],
                        'reliability': source.get('reliability', 0.5),
                        'extracted_at': datetime.now(timezone.utc).isoformat(),
                        'extraction_method': 'advanced_selectors'
                    })
                
            except Exception as e:
                logger.debug(f"⚠️ Container processing error: {e}")
                continue
        
        return results
    
    def _extract_title_advanced(self, container, selectors: Dict[str, str]) -> str:
        """Advanced title extraction with multiple fallbacks"""
        title_selectors = [
            selectors.get('title', ''),
            'h1, h2, h3, h4',
            '.title, .headline, .name',
            'a[href*="airdrop"]',
            '[data-title]',
            '.post-title, .article-title'
        ]
        
        for selector in title_selectors:
            if not selector:
                continue
                
            try:
                elements = container.select(selector)
                for elem in elements:
                    title = elem.get_text(strip=True)
                    if title and len(title) >= 8:
                        # Clean title
                        title = re.sub(r'\s+', ' ', title)
                        title = re.sub(r'[^\w\s\-\(\)\[\]\.,:;!?]', '', title)
                        return title
            except:
                continue
        
        return ""
    
    def _extract_description_advanced(self, container, selectors: Dict[str, str]) -> str:
        """Advanced description extraction"""
        desc_selectors = [
            selectors.get('description', ''),
            'p, .description, .summary, .excerpt',
            '.content, .text, .body',
            '[data-description]'
        ]
        
        descriptions = []
        
        for selector in desc_selectors:
            if not selector:
                continue
                
            try:
                elements = container.select(selector)
                for elem in elements[:3]:  # Limit to first 3 elements
                    text = elem.get_text(strip=True)
                    if text and len(text) > 20:
                        descriptions.append(text)
            except:
                continue
        
        # Combine and clean descriptions
        if descriptions:
            full_desc = ' '.join(descriptions)
            full_desc = re.sub(r'\s+', ' ', full_desc)
            return full_desc
        
        return ""
    
    def _extract_url_advanced(self, container, base_url: str) -> str:
        """Advanced URL extraction with validation"""
        url_selectors = [
            'a[href]',
            '[data-url]',
            '[data-link]'
        ]
        
        for selector in url_selectors:
            try:
                elements = container.select(selector)
                for elem in elements:
                    href = elem.get('href') or elem.get('data-url') or elem.get('data-link')
                    if href:
                        # Convert relative URLs to absolute
                        if href.startswith('http'):
                            return href
                        elif href.startswith('/'):
                            return urljoin(base_url, href)
            except:
                continue
        
        return base_url
    
    def _validate_content_quality(self, title: str, description: str) -> bool:
        """Validate content quality using multiple criteria"""
        # Length validation
        if len(title) < 8 or len(title) > 300:
            return False
        
        # Airdrop relevance check
        text = f"{title} {description}".lower()
        
        # Strong airdrop indicators
        strong_indicators = [
            'airdrop', 'token distribution', 'free tokens', 'claim tokens',
            'testnet reward', 'mainnet launch', 'token allocation', 'free crypto'
        ]
        
        if any(indicator in text for indicator in strong_indicators):
            return True
        
        # Weak indicators (need multiple)
        weak_indicators = [
            'token', 'crypto', 'blockchain', 'launch', 'reward', 'testnet',
            'mainnet', 'defi', 'nft', 'web3', 'dapp'
        ]
        
        weak_count = sum(1 for indicator in weak_indicators if indicator in text)
        
        # Spam/low-quality filters
        spam_patterns = [
            'click here', 'buy now', 'limited time', 'act fast',
            'guaranteed profit', 'get rich', 'double your'
        ]
        
        if any(pattern in text for pattern in spam_patterns):
            return False
        
        return weak_count >= 2
    
    def _intelligent_content_discovery(self, soup: BeautifulSoup, source: Dict[str, Any], 
                                     url: str) -> List[Dict[str, Any]]:
        """Intelligent content discovery using ML-guided extraction"""
        results = []
        
        # Look for airdrop-related content using semantic analysis
        airdrop_patterns = [
            r'airdrop.*(?:token|crypto|reward)',
            r'(?:free|claim).*token',
            r'testnet.*reward',
            r'mainnet.*launch.*token'
        ]
        
        # Find relevant sections
        relevant_sections = []
        for pattern in airdrop_patterns:
            elements = soup.find_all(text=re.compile(pattern, re.IGNORECASE))
            for elem in elements:
                parent = elem.parent
                for _ in range(3):  # Go up 3 levels to find container
                    if parent and parent.name in ['div', 'article', 'section', 'li']:
                        relevant_sections.append(parent)
                        break
                    parent = parent.parent if parent else None
        
        # Extract from relevant sections
        for section in relevant_sections[:10]:  # Limit to 10 sections
            try:
                # Extract title
                title_elem = section.find(['h1', 'h2', 'h3', 'h4'])
                if not title_elem:
                    title_elem = section.find(['a', 'strong', 'b'])
                
                title = title_elem.get_text(strip=True) if title_elem else ""
                
                if len(title) >= 8:
                    # Extract description
                    description = section.get_text(strip=True)[:500]
                    
                    # Extract URL
                    link_elem = section.find('a', href=True)
                    item_url = urljoin(url, link_elem['href']) if link_elem else url
                    
                    if self._validate_content_quality(title, description):
                        results.append({
                            'title': title,
                            'description': description,
                            'url': item_url,
                            'source': source['name'] + ' (AI)',
                            'reliability': max(0.3, source.get('reliability', 0.5) - 0.2),
                            'extracted_at': datetime.now(timezone.utc).isoformat(),
                            'extraction_method': 'intelligent_discovery'
                        })
                        
            except Exception as e:
                logger.debug(f"⚠️ Intelligent discovery error: {e}")
                continue
        
        return results[:8]  # Limit intelligent discovery results
    
    async def _extract_from_api_async(self, url: str, source: Dict[str, Any], 
                                    session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Extract from JSON API sources asynchronously"""
        response_data = await self.scraper.async_stealth_get(url, session)
        
        if not response_data or response_data['status'] != 200:
            return []
        
        try:
            data = json.loads(response_data['content'])
            results = []
            
            # Handle different API response structures
            items = self._extract_items_from_api_response(data)
            
            for item in items[:25]:  # Limit API results
                if isinstance(item, dict):
                    title = self._extract_api_field(item, ['title', 'name', 'headline'])
                    description = self._extract_api_field(item, ['description', 'summary', 'content', 'body'])
                    item_url = self._extract_api_field(item, ['url', 'link', 'href'])
                    
                    if title and self._validate_content_quality(title, description or ""):
                        results.append({
                            'title': str(title)[:300],
                            'description': str(description or '')[:800],
                            'url': item_url or url,
                            'source': source['name'] + ' (API)',
                            'reliability': source.get('reliability', 0.8),  # APIs typically more reliable
                            'extracted_at': datetime.now(timezone.utc).isoformat(),
                            'extraction_method': 'api'
                        })
            
            return results
            
        except (json.JSONDecodeError, Exception) as e:
            logger.debug(f"⚠️ API parsing error for {url}: {e}")
            return []
    
    def _extract_items_from_api_response(self, data: Any) -> List[Dict]:
        """Extract items from various API response structures"""
        if isinstance(data, list):
            return data
        
        if isinstance(data, dict):
            # Try common API patterns
            for key in ['data', 'items', 'results', 'posts', 'articles', 'entries', 'children']:
                if key in data:
                    value = data[key]
                    if isinstance(value, list):
                        return value
                    elif isinstance(value, dict) and 'data' in value:
                        return value['data'] if isinstance(value['data'], list) else [value['data']]
            
            # Reddit-specific structure
            if 'data' in data and 'children' in data['data']:
                return [child['data'] for child in data['data']['children'] if 'data' in child]
        
        return []
    
    def _extract_api_field(self, item: Dict, field_names: List[str]) -> Optional[str]:
        """Extract field from API item with multiple fallbacks"""
        for field_name in field_names:
            if field_name in item and item[field_name]:
                value = item[field_name]
                return str(value) if value else None
        return None
    
    async def _extract_from_rss_async(self, url: str, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract from RSS feeds asynchronously"""
        try:
            import feedparser
            
            # Use asyncio to run feedparser in thread pool
            loop = asyncio.get_event_loop()
            feed = await loop.run_in_executor(None, feedparser.parse, url)
            
            results = []
            
            for entry in feed.entries[:20]:  # Limit RSS results
                title = getattr(entry, 'title', '')
                description = getattr(entry, 'description', '') or getattr(entry, 'summary', '')
                link = getattr(entry, 'link', url)
                
                if title and self._validate_content_quality(title, description):
                    results.append({
                        'title': title[:300],
                        'description': description[:800],
                        'url': link,
                        'source': source['name'] + ' (RSS)',
                        'reliability': source.get('reliability', 0.7),
                        'extracted_at': datetime.now(timezone.utc).isoformat(),
                        'extraction_method': 'rss'
                    })
            
            return results
            
        except ImportError:
            logger.warning("⚠️ feedparser not available for RSS extraction")
            return []
        except Exception as e:
            logger.debug(f"⚠️ RSS parsing error for {url}: {e}")
            return []
    
    def _apply_source_specific_processing(self, results: List[Dict[str, Any]], 
                                        source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply source-specific post-processing"""
        source_name = source['name'].lower()
        
        # Source-specific cleaning and enhancement
        if 'reddit' in source_name:
            results = self._process_reddit_results(results)
        elif 'github' in source_name:
            results = self._process_github_results(results)
        elif 'coingecko' in source_name:
            results = self._process_coingecko_results(results)
        
        return results
    
    def _process_reddit_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process Reddit-specific results"""
        processed = []
        
        for result in results:
            # Reddit-specific title cleaning
            title = result.get('title', '')
            title = re.sub(r'^\[.*?\]\s*', '', title)  # Remove [flair] tags
            title = re.sub(r'(?i)^(daily|weekly|monthly)\s+', '', title)  # Remove recurring post indicators
            
            # Skip Reddit meta posts
            if any(skip_term in title.lower() for skip_term in ['daily thread', 'weekly discussion', 'monthly recap']):
                continue
            
            result['title'] = title
            processed.append(result)
        
        return processed
    
    def _process_github_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process GitHub-specific results"""
        processed = []
        
        for result in results:
            # Enhance GitHub results with additional context
            description = result.get('description', '')
            if 'github.com' in result.get('url', ''):
                result['extraction_method'] += '_github'
                # GitHub repos get slight reliability boost for open source transparency
                result['reliability'] = min(1.0, result.get('reliability', 0.5) + 0.1)
            
            processed.append(result)
        
        return processed
    
    def _process_coingecko_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process CoinGecko-specific results"""
        processed = []
        
        for result in results:
            # CoinGecko gets highest reliability boost
            result['reliability'] = min(1.0, result.get('reliability', 0.8) + 0.15)
            
            # Clean CoinGecko-specific formatting
            title = result.get('title', '')
            title = re.sub(r'(?i)\s*\|\s*coingecko$', '', title)
            result['title'] = title
            
            processed.append(result)
        
        return processed
    
    def _apply_advanced_filtering(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply advanced filtering with ML-based quality assessment"""
        if not results:
            return results
        
        logger.info(f"🔍 Applying advanced filtering to {len(results)} raw items...")
        
        # Step 1: Basic quality filtering
        filtered_results = []
        for result in results:
            if self._passes_quality_filter(result):
                filtered_results.append(result)
        
        logger.info(f"📋 After quality filtering: {len(filtered_results)} items")
        
        # Step 2: ML-based content assessment
        assessed_results = []
        for result in filtered_results:
            try:
                # Quick ML assessment for relevance
                relevance_score = self._assess_airdrop_relevance(result)
                if relevance_score >= 0.3:  # Minimum relevance threshold
                    result['relevance_score'] = relevance_score
                    assessed_results.append(result)
                    
            except Exception as e:
                logger.debug(f"⚠️ ML assessment failed: {e}")
                # Include without assessment if ML fails
                result['relevance_score'] = 0.5
                assessed_results.append(result)
        
        logger.info(f"🧠 After ML assessment: {len(assessed_results)} items")
        
        # Step 3: Advanced deduplication
        deduplicated_results = self._advanced_deduplication(assessed_results)
        
        logger.success(f"✨ Final filtered results: {len(deduplicated_results)} high-quality items")
        
        return deduplicated_results
    
    def _passes_quality_filter(self, result: Dict[str, Any]) -> bool:
        """Check if result passes basic quality filters"""
        title = result.get('title', '')
        description = result.get('description', '')
        
        # Length requirements
        if len(title) < 5 or len(title) > 500:
            return False
        
        # Spam detection
        spam_indicators = [
            'click here now', 'limited time offer', 'act fast',
            'guaranteed money', 'double your crypto', 'ponzi',
            'pyramid scheme', 'mlm opportunity'
        ]
        
        full_text = f"{title} {description}".lower()
        if any(spam in full_text for spam in spam_indicators):
            return False
        
        # Language check (basic English detection)
        english_indicators = ['the', 'and', 'or', 'for', 'to', 'a', 'an']
        if not any(word in full_text for word in english_indicators):
            # Allow non-English but boost English content
            pass
        
        return True
    
    def _assess_airdrop_relevance(self, result: Dict[str, Any]) -> float:
        """Assess airdrop relevance using lightweight ML"""
        title = result.get('title', '').lower()
        description = result.get('description', '').lower()
        full_text = f"{title} {description}"
        
        relevance_score = 0.0
        
        # High-relevance keywords
        high_relevance = [
            'airdrop', 'token distribution', 'free tokens', 'claim tokens',
            'testnet reward', 'mainnet launch', 'token allocation'
        ]
        
        # Medium-relevance keywords
        medium_relevance = [
            'crypto', 'blockchain', 'defi', 'nft', 'web3', 'dapp',
            'ethereum', 'polygon', 'solana', 'cardano'
        ]
        
        # Context boosters
        context_boosters = [
            'whitepaper', 'github', 'audit', 'team', 'partnership',
            'roadmap', 'tokenomics', 'staking', 'governance'
        ]
        
        # Calculate relevance
        high_count = sum(1 for term in high_relevance if term in full_text)
        medium_count = sum(1 for term in medium_relevance if term in full_text)
        context_count = sum(1 for term in context_boosters if term in full_text)
        
        relevance_score = (
            high_count * 0.4 +
            medium_count * 0.2 +
            context_count * 0.1
        )
        
        # Source reliability boost
        source_reliability = result.get('reliability', 0.5)
        relevance_score += source_reliability * 0.2
        
        # Title prominence boost
        if any(term in title for term in high_relevance):
            relevance_score += 0.15
        
        return min(1.0, relevance_score)
    
    def _advanced_deduplication(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Advanced deduplication using multiple similarity metrics"""
        if len(results) <= 1:
            return results
        
        deduplicated = []
        seen_signatures = set()
        
        for result in results:
            # Create multiple similarity signatures
            title_signature = self._create_title_signature(result['title'])
            url_signature = self._create_url_signature(result.get('url', ''))
            content_signature = self._create_content_signature(result)
            
            # Combined signature
            combined_signature = f"{title_signature}|{url_signature}"
            
            # Check for duplicates
            is_duplicate = False
            
            # Exact signature match
            if combined_signature in seen_signatures:
                is_duplicate = True
            else:
                # Fuzzy similarity check
                for existing_result in deduplicated:
                    similarity = self._calculate_result_similarity(result, existing_result)
                    if similarity > 0.85:  # High similarity threshold
                        is_duplicate = True
                        # Keep the one with higher reliability
                        if result.get('reliability', 0) > existing_result.get('reliability', 0):
                            deduplicated.remove(existing_result)
                            is_duplicate = False
                        break
            
            if not is_duplicate:
                deduplicated.append(result)
                seen_signatures.add(combined_signature)
        
        return deduplicated
    
    def _create_title_signature(self, title: str) -> str:
        """Create normalized title signature for deduplication"""
        # Normalize title
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = [word for word in normalized.split() if word not in common_words]
        
        return ' '.join(sorted(words))
    
    def _create_url_signature(self, url: str) -> str:
        """Create URL signature for deduplication"""
        if not url:
            return ""
        
        try:
            parsed = urlparse(url)
            # Use domain + path (ignore query parameters and fragments)
            return f"{parsed.netloc}{parsed.path}".lower()
        except:
            return url.lower()
    
    def _create_content_signature(self, result: Dict[str, Any]) -> str:
        """Create content-based signature"""
        title = result.get('title', '')
        description = result.get('description', '')
        
        # Combine and normalize
        content = f"{title} {description}".lower()
        content = re.sub(r'[^\w\s]', '', content)
        content = re.sub(r'\s+', ' ', content)
        
        # Create hash of normalized content
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _calculate_result_similarity(self, result1: Dict[str, Any], result2: Dict[str, Any]) -> float:
        """Calculate similarity between two results"""
        try:
            from fuzzywuzzy import fuzz
            
            title1 = result1.get('title', '').lower()
            title2 = result2.get('title', '').lower()
            
            # Multiple similarity metrics
            ratio = fuzz.ratio(title1, title2) / 100
            token_sort = fuzz.token_sort_ratio(title1, title2) / 100
            token_set = fuzz.token_set_ratio(title1, title2) / 100
            
            # Weighted average
            similarity = (ratio * 0.3 + token_sort * 0.4 + token_set * 0.3)
            
            # URL similarity boost
            url1 = result1.get('url', '')
            url2 = result2.get('url', '')
            if url1 and url2:
                url_similarity = fuzz.ratio(url1, url2) / 100
                similarity = (similarity * 0.8 + url_similarity * 0.2)
            
            return similarity
            
        except ImportError:
            # Fallback: simple token matching
            title1_tokens = set(result1.get('title', '').lower().split())
            title2_tokens = set(result2.get('title', '').lower().split())
            
            if not title1_tokens or not title2_tokens:
                return 0.0
            
            intersection = len(title1_tokens & title2_tokens)
            union = len(title1_tokens | title2_tokens)
            
            return intersection / union if union > 0 else 0.0
    
    def get_extraction_stats(self) -> Dict[str, Any]:
        """Get detailed extraction performance statistics"""
        total_extractions = self.performance_stats['extractions']
        
        return {
            'total_extractions': total_extractions,
            'successful_extractions': self.performance_stats['successful'],
            'failed_extractions': self.performance_stats['failed'],
            'success_rate': (self.performance_stats['successful'] / total_extractions * 100) if total_extractions > 0 else 0,
            'cache_hit_rate': (self.performance_stats['cached_hits'] / total_extractions * 100) if total_extractions > 0 else 0,
            'avg_processing_time': self.performance_stats['avg_processing_time'],
            'cache_size': len(self.extraction_cache)
        }

# ═══════════════════════════════════════════════════════════════════════════════════════
# 📱 SUPREME MULTI-CHANNEL NOTIFICATION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════════════

class SupremeNotificationSystem:
    """Advanced multi-channel notification system with intelligent routing"""
    
    def __init__(self):
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        self.discord_webhook = os.environ.get('DISCORD_WEBHOOK')
        self.github_token = os.environ.get('GITHUB_TOKEN')
        
        self.notification_stats = {
            'telegram': {'sent': 0, 'failed': 0},
            'discord': {'sent': 0, 'failed': 0},
            'github': {'sent': 0, 'failed': 0}
        }
    
    async def send_comprehensive_notifications(self, airdrops: List[Dict[str, Any]], 
                                             collection_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Send notifications through all configured channels"""
        logger.info("📱 Sending comprehensive notifications...")
        
        notification_results = {}
        
        # Prepare notification content
        if airdrops:
            content = self._prepare_rich_content(airdrops, collection_stats)
        else:
            content = self._prepare_no_results_content(collection_stats)
        
        # Send notifications concurrently
        tasks = []
        
        if self.telegram_token and self.telegram_chat_id:
            tasks.append(self._send_telegram_notification(content['telegram']))
        
        if self.discord_webhook:
            tasks.append(self._send_discord_notification(content['discord'], airdrops))
        
        if self.github_token and airdrops:
            tasks.append(self._create_github_intelligence_report(airdrops, collection_stats))
        
        # Execute all notifications concurrently
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            channels = ['telegram', 'discord', 'github']
            for i, result in enumerate(results):
                if i < len(channels):
                    channel = channels[i]
                    if isinstance(result, Exception):
                        notification_results[channel] = {'success': False, 'error': str(result)}
                        self.notification_stats[channel]['failed'] += 1
                    else:
                        notification_results[channel] = {'success': True, 'data': result}
                        self.notification_stats[channel]['sent'] += 1
        
        logger.success(f"📡 Notifications sent: {sum(1 for r in notification_results.values() if r.get('success'))}/{len(notification_results)}")
        
        return notification_results
    
    def _prepare_rich_content(self, airdrops: List[Dict[str, Any]], 
                            stats: Dict[str, Any]) -> Dict[str, str]:
        """Prepare rich content for different notification channels"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        
        # Sort airdrops by priority and legitimacy
        sorted_airdrops = sorted(airdrops, key=lambda x: (
            x.get('priority_score', 0),
            x.get('legitimacy_score', 0),
            x.get('value_score', 0)
        ), reverse=True)
        
        # Telegram content (HTML formatting)
        telegram_content = f"""🚀 <b>SUPREME AIRDROP INTELLIGENCE REPORT</b>

🕒 <b>Timestamp:</b> {timestamp}
📊 <b>Collection Summary:</b>
├ 🎯 New Discoveries: {len(airdrops)}
├ ⚡ Sources Scanned: {stats.get('total_sources', 0)}
├ 🔍 Items Analyzed: {stats.get('total_items_found', 0)}
├ 🔄 Duplicates Filtered: {stats.get('duplicates_filtered', 0)}
└ ⏱️ Processing Time: {stats.get('processing_time_seconds', 0):.1f}s

🎯 <b>TOP PRIORITY OPPORTUNITIES:</b>
"""
        
        for i, airdrop in enumerate(sorted_airdrops[:6], 1):
            title = airdrop.get('title', 'Unknown')[:45]
            category = airdrop.get('category', 'Other')
            priority = airdrop.get('priority_score', 0)
            legitimacy = airdrop.get('legitimacy_score', 0)
            risk_level = airdrop.get('risk_level', 'Unknown')
            value_category = airdrop.get('value_category', 'Unknown')
            
            telegram_content += f"""
{i}. <b>{title}</b>
   📂 {category} | 🎯 {priority}/5 | ✅ {legitimacy}/100
   ⚠️ Risk: {risk_level} | 💎 Value: {value_category}
   🔗 <i>{airdrop.get('source', 'Unknown')}</i>
"""
        
        telegram_content += f"""

💰 <b>Target Wallet:</b> <code>{CONFIG.WALLET_ADDRESS}</code>

🛡️ <b>SECURITY PROTOCOL:</b>
• All discoveries require manual verification
• Never share private keys or seed phrases  
• Research projects thoroughly before participation
• Use dedicated airdrop wallet for safety

📊 <b>Full Intelligence Report:</b> Check GitHub for detailed analysis
🔄 <b>Next Scan:</b> Automated monitoring continues...
"""
        
        # Discord content (more structured)
        discord_content = f"""🎯 **SUPREME AIRDROP INTELLIGENCE REPORT**

⏰ **Scan Completed:** {timestamp}
📈 **Performance:** {len(airdrops)} new opportunities discovered
🎯 **Success Rate:** {stats.get('success_rate', 0):.1f}%

**🏆 Top Priority Discoveries:**
{chr(10).join([f"{i+1}. **{airdrop.get('title', 'Unknown')[:50]}** (Priority: {airdrop.get('priority_score', 0)}/5)" for i, airdrop in enumerate(sorted_airdrops[:5])])}

**📊 Collection Statistics:**
• Sources Scanned: {stats.get('total_sources', 0)}
• Items Analyzed: {stats.get('total_items_found', 0)}  
• Processing Time: {stats.get('processing_time_seconds', 0):.1f}s

**🎯 Target Wallet:** `{CONFIG.WALLET_ADDRESS}`
"""
        
        return {
            'telegram': telegram_content,
            'discord': discord_content
        }
    
    def _prepare_no_results_content(self, stats: Dict[str, Any]) -> Dict[str, str]:
        """Prepare content when no new airdrops are found"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        
        telegram_content = f"""🤖 <b>STEALTH MONITORING REPORT</b>

🕒 <b>Timestamp:</b> {timestamp}
📊 <b>Status:</b> No new opportunities detected
⚡ <b>Sources Monitored:</b> {stats.get('total_sources', 0)}
🔍 <b>Items Analyzed:</b> {stats.get('total_items_found', 0)}
💫 <b>Duplicates Filtered:</b> {stats.get('duplicates_filtered', 0)}
⏱️ <b>Processing Time:</b> {stats.get('processing_time_seconds', 0):.1f}s

💰 <b>Wallet:</b> <code>{CONFIG.WALLET_ADDRESS}</code>

🔄 <b>Continuous monitoring active...</b>
Next comprehensive scan in 4-6 hours.
"""
        
        discord_content = f"""🤖 **STEALTH MONITORING REPORT**

⏰ **Scan Completed:** {timestamp}
📊 **Status:** No new opportunities detected
🔍 **Analysis:** {stats.get('total_items_found', 0)} items scanned, {stats.get('duplicates_filtered', 0)} duplicates filtered

**🎯 Target Wallet:** `{CONFIG.WALLET_ADDRESS}`
**🔄 Next Scan:** Automated monitoring continues...
"""
        
        return {
            'telegram': telegram_content,
            'discord': discord_content
        }
    
    async def _send_telegram_notification(self, content: str) -> Dict[str, Any]:
        """Send Telegram notification with retry logic"""
        if not self.telegram_token or not self.telegram_chat_id:
            return {'success': False, 'error': 'Telegram not configured'}
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        
        # Split long messages
        max_length = 4000
        messages = [content[i:i+max_length] for i in range(0, len(content), max_length)]
        
        try:
            async with aiohttp.ClientSession() as session:
                for i, message in enumerate(messages):
                    payload = {
                        'chat_id': self.telegram_chat_id,
                        'text': message,
                        'parse_mode': 'HTML',
                        'disable_web_page_preview': True
                    }
                    
                    async with session.post(url, json=payload, timeout=30) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            raise Exception(f"Telegram API error: {response.status} - {error_text}")
                    
                    # Rate limiting between messages
                    if i < len(messages) - 1:
                        await asyncio.sleep(1)
            
            logger.success("📱 Telegram notification sent successfully")
            return {'success': True, 'messages_sent': len(messages)}
            
        except Exception as e:
            logger.error(f"❌ Telegram notification failed: {e}")
            raise e
    
    async def _send_discord_notification(self, content: str, airdrops: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Send Discord webhook notification with rich embeds"""
        if not self.discord_webhook:
            return {'success': False, 'error': 'Discord webhook not configured'}
        
        try:
            # Create rich embed
            embed = {
                "title": "🚀 Supreme Airdrop Intelligence Report",
                "description": content[:2000],  # Discord embed description limit
                "color": 0x00ff88 if airdrops else 0xffa500,  # Green for results, orange for no results
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "footer": {
                    "text": f"Supreme Airdrop Collector v{CONFIG.VERSION}",
                    "icon_url": "https://cdn.discordapp.com/emojis/123456789.png"
                },
                "thumbnail": {
                    "url": "https://cryptologos.cc/logos/ethereum-eth-logo.png"
                }
            }
            
            # Add fields for top airdrops
            if airdrops:
                embed["fields"] = []
                
                # Summary field
                embed["fields"].append({
                    "name": "📊 Summary",
                    "value": f"**New Opportunities:** {len(airdrops)}\n**Target Wallet:** `{CONFIG.WALLET_ADDRESS[:20]}...`",
                    "inline": False
                })
                
                # Top airdrops
                for i, airdrop in enumerate(airdrops[:4], 1):
                    title = airdrop.get('title', 'Unknown')[:50]
                    category = airdrop.get('category', 'Other')
                    priority = airdrop.get('priority_score', 0)
                    legitimacy = airdrop.get('legitimacy_score', 0)
                    risk_level = airdrop.get('risk_level', 'Unknown')
                    
                    embed["fields"].append({
                        "name": f"{i}. {title}",
                        "value": f"**Category:** {category}\n**Priority:** {priority}/5 ⭐\n**Legitimacy:** {legitimacy}/100 ✅\n**Risk:** {risk_level} ⚠️",
                        "inline": True
                    })
            
            payload = {"embeds": [embed]}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.discord_webhook, json=payload, timeout=30) as response:
                    if response.status == 204:
                        logger.success("💬 Discord notification sent successfully")
                        return {'success': True, 'webhook_response': response.status}
                    else:
                        error_text = await response.text()
                        raise Exception(f"Discord webhook error: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"❌ Discord notification failed: {e}")
            raise e
    
    async def _create_github_intelligence_report(self, airdrops: List[Dict[str, Any]], 
                                               stats: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive GitHub intelligence report"""
        if not self.github_token:
            return {'success': False, 'error': 'GitHub token not configured'}
        
        try:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            title = f"🎯 Supreme Airdrop Intelligence Report - {len(airdrops)} Opportunities - {timestamp}"
            
            # Generate comprehensive report body
            body = self._generate_github_report_body(airdrops, stats, timestamp)
            
            url = f"https://api.github.com/repos/{CONFIG.REPO_OWNER}/{CONFIG.REPO_NAME}/issues"
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Supreme-Airdrop-Collector/3.0'
            }
            
            payload = {
                'title': title,
                'body': body,
                'labels': [
                    'airdrop-intelligence',
                    'automated-report', 
                    'high-priority' if len(airdrops) > 5 else 'standard-scan',
                    'review-required'
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=60) as response:
                    if response.status == 201:
                        issue_data = await response.json()
                        issue_number = issue_data['number']
                        issue_url = issue_data['html_url']
                        
                        logger.success(f"📋 GitHub issue #{issue_number} created: {issue_url}")
                        return {
                            'success': True, 
                            'issue_number': issue_number,
                            'issue_url': issue_url
                        }
                    else:
                        error_text = await response.text()
                        raise Exception(f"GitHub API error: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"❌ GitHub report creation failed: {e}")
            raise e
    
    def _generate_github_report_body(self, airdrops: List[Dict[str, Any]], 
                                   stats: Dict[str, Any], timestamp: str) -> str:
        """Generate comprehensive GitHub report body"""
        # Sort airdrops by intelligence score
        sorted_airdrops = sorted(airdrops, key=lambda x: (
            x.get('priority_score', 0),
            x.get('legitimacy_score', 0),
            x.get('confidence_level', 0)
        ), reverse=True)
        
        body = f"""# 🎯 Supreme Airdrop Intelligence Report

**Generated:** {timestamp}  
**Version:** {CONFIG.VERSION}  
**New Opportunities:** {len(airdrops)}  
**Target Wallet:** `{CONFIG.WALLET_ADDRESS}`  

## 📊 Collection Intelligence Summary

| Metric | Value |
|--------|-------|
| 🎯 **Sources Scanned** | {stats.get('total_sources', 0)} |
| 🔍 **Items Analyzed** | {stats.get('total_items_found', 0)} |
| ✨ **New Opportunities** | {stats.get('new_airdrops', 0)} |
| 🔄 **Duplicates Filtered** | {stats.get('duplicates_filtered', 0)} |
| ⏱️ **Processing Time** | {stats.get('processing_time_seconds', 0):.2f}s |
| 📈 **Success Rate** | {stats.get('success_rate', 0):.1f}% |
| 🧠 **ML Confidence** | {stats.get('avg_confidence', 0):.1f}% |

## 🚀 High-Priority Intelligence Discoveries

"""
        
        # Add detailed analysis for each airdrop
        for i, airdrop in enumerate(sorted_airdrops[:15], 1):
            body += f"""### {i}. {airdrop.get('title', 'Unknown Opportunity')}

**📋 Intelligence Summary:**
- **🎯 Priority Score:** {airdrop.get('priority_score', 0)}/5 ⭐
- **✅ Legitimacy Score:** {airdrop.get('legitimacy_score', 0)}/100
- **⚠️ Risk Level:** {airdrop.get('risk_level', 'Unknown')}
- **📂 Category:** {airdrop.get('category', 'Other')}
- **💎 Value Estimate:** {airdrop.get('value_category', 'Unknown')} ({airdrop.get('estimated_value_range', 'N/A')})
- **⏱️ Time Requirement:** {airdrop.get('time_requirement_category', 'Unknown')} ({airdrop.get('time_estimate', 'N/A')})
- **🧠 ML Confidence:** {airdrop.get('confidence_level', 0) * 100:.1f}%
- **📡 Source:** {airdrop.get('source', 'Unknown')} (Reliability: {airdrop.get('reliability', 0) * 100:.0f}%)

**🔗 Access URL:** {airdrop.get('url', 'N/A')}

**📝 Description:**
{airdrop.get('description', 'No description available')[:500]}{'...' if len(airdrop.get('description', '')) > 500 else ''}

**🔍 Key Insights:**
{chr(10).join([f"- {insight}" for insight in airdrop.get('key_insights', ['Manual analysis required'])])}

**🟢 Positive Indicators:**
{chr(10).join([f"- {flag}" for flag in airdrop.get('green_flags', [])]) if airdrop.get('green_flags') else "- None detected"}

**🔴 Risk Flags:**
{chr(10).join([f"- {flag}" for flag in airdrop.get('red_flags', [])]) if airdrop.get('red_flags') else "- None detected"}

**🤖 AI Recommendation:** {airdrop.get('recommendation', 'Manual review required')}

---

"""
        
        # Add performance analytics
        body += f"""## 📈 Collection Performance Analytics

### 🎯 Source Performance
{self._generate_source_performance_table(stats)}

### 🧠 ML Analysis Performance
- **Average Processing Time:** {stats.get('avg_ml_processing_time', 0):.3f}s per item
- **Confidence Distribution:** 
  - High Confidence (>80%): {stats.get('high_confidence_count', 0)} items
  - Medium Confidence (50-80%): {stats.get('medium_confidence_count', 0)} items  
  - Low Confidence (<50%): {stats.get('low_confidence_count', 0)} items

### 📊 Category Distribution
{self._generate_category_distribution(sorted_airdrops)}

## ⚠️ CRITICAL SECURITY PROTOCOL

### 🛡️ **MANDATORY SECURITY CHECKLIST**

**❌ NEVER DO:**
- Share private keys or seed phrases with anyone
- Send ETH, tokens, or crypto to unknown addresses
- Download suspicious files or run unknown software
- Connect your main wallet to unverified dApps
- Participate without thorough research

**✅ ALWAYS DO:**
1. **🔍 Research Thoroughly** - Verify team, partnerships, and project legitimacy
2. **📋 Check Official Channels** - Confirm through official website/social media
3. **🔐 Use Dedicated Wallet** - Create separate wallet for airdrop activities
4. **🛡️ Verify Smart Contracts** - Check on Etherscan or equivalent explorers
5. **👥 Community Validation** - Check community feedback and reviews
6. **⏰ No Rush Decisions** - Legitimate airdrops don't require urgent action

### 📋 Verification Workflow

For each opportunity above:

1. **Project Research**
   - [ ] Team verification and background check
   - [ ] Whitepaper and technical documentation review
   - [ ] Partnership and investor validation
   - [ ] Community size and engagement analysis

2. **Technical Verification**
   - [ ] Smart contract audit reports
   - [ ] Code repository accessibility (GitHub)
   - [ ] Tokenomics and distribution model
   - [ ] Security measures implementation

3. **Risk Assessment**
   - [ ] Red flags evaluation
   - [ ] Regulatory compliance check
   - [ ] Market conditions analysis
   - [ ] Historical team performance

**🎯 Target Wallet Address:** `{CONFIG.WALLET_ADDRESS}`

---

*🤖 Generated by Supreme Airdrop Collector v{CONFIG.VERSION}*  
*⚡ Powered by Advanced ML Intelligence & Quantum Security*  
*🛡️ For Educational and Research Purposes Only*

**Next automated scan scheduled in 4-6 hours**
"""
        
        return body
    
    def _generate_source_performance_table(self, stats: Dict[str, Any]) -> str:
        """Generate source performance markdown table"""
        top_sources = stats.get('top_sources', {})
        
        if not top_sources:
            return "No source performance data available."
        
        table = "| Source | Items Found | Success Rate | Avg Quality |\n"
        table += "|--------|-------------|--------------|-------------|\n"
        
        for source, data in top_sources.items():
            items = data.get('items', 0)
            success_rate = data.get('success_rate', 0)
            quality = data.get('avg_quality', 0)
            table += f"| {source} | {items} | {success_rate:.1f}% | {quality:.1f}/5 |\n"
        
        return table
    
    def _generate_category_distribution(self, airdrops: List[Dict[str, Any]]) -> str:
        """Generate category distribution table"""
        categories = {}
        for airdrop in airdrops:
            category = airdrop.get('category', 'Other')
            if category not in categories:
                categories[category] = {'count': 0, 'avg_priority': 0, 'total_priority': 0}
            
            categories[category]['count'] += 1
            priority = airdrop.get('priority_score', 0)
            categories[category]['total_priority'] += priority
            categories[category]['avg_priority'] = categories[category]['total_priority'] / categories[category]['count']
        
        if not categories:
            return "No category data available."
        
        table = "| Category | Count | Avg Priority | Percentage |\n"
        table += "|----------|-------|--------------|------------|\n"
        
        total_count = sum(cat['count'] for cat in categories.values())
        
        for category, data in sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True):
            count = data['count']
            avg_priority = data['avg_priority']
            percentage = (count / total_count) * 100
            table += f"| {category} | {count} | {avg_priority:.1f}/5 | {percentage:.1f}% |\n"
        
        return table
    
    def get_notification_stats(self) -> Dict[str, Any]:
        """Get notification system statistics"""
        return {
            'channels_configured': sum(1 for channel in ['telegram', 'discord', 'github'] 
                                     if getattr(self, f"{channel}_token" if channel == 'github' 
                                               else f"{channel}_webhook" if channel == 'discord' 
                                               else f"{channel}_token", None)),
            'total_sent': sum(stats['sent'] for stats in self.notification_stats.values()),
            'total_failed': sum(stats['failed'] for stats in self.notification_stats.values()),
            'channel_stats': self.notification_stats
        }

# Continue to part 3...