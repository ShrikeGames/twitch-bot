from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter,BestMatch
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import random
from chatterbot import filters
from chatterbot.conversation import Statement

class BotChanLogicAdapter(BestMatch):
	def __init__(self, chatbot, **kwargs):
		super().__init__(chatbot, **kwargs)
	
	def compare_statements(self, input_statement, other_statement):
		statement_text = str(input_statement.text.lower())
		other_statement_text = str(other_statement.text.lower())
		ratio=fuzz.ratio(statement_text,other_statement_text)
		partial_ratio=fuzz.ratio(statement_text,other_statement_text)
		result=((ratio*0.8)+(partial_ratio*0.2))
		
		input_parts=statement_text.split(' ')
		max_partial=result
		for part in input_parts:
			if part in other_statement_text:
				ratio=fuzz.ratio(statement_text,part)
				partial_ratio=fuzz.ratio(statement_text,part)
				result=((ratio*0.8)+(partial_ratio*0.2))
				if result > max_partial:
					max_partial = result
		
		return max_partial
	def process(self, input_statement, additional_response_selection_parameters=None):
		search_results = self.search_algorithm.search(input_statement)

		# Use the input statement as the closest match if no other results are found
		closest_match = next(search_results, input_statement)
		
		# Search for the closest match to the input statement
		for result in search_results:
			# Stop searching if a match that is close enough is found
			if result.confidence >= self.maximum_similarity_threshold:
				closest_match = result
				break

		recent_repeated_responses = filters.get_recent_repeated_responses(
			self.chatbot,
			input_statement.conversation
		)
		print('closest_match',closest_match)
		print("self.maximum_similarity_threshold",self.maximum_similarity_threshold)
		response_selection_parameters = {
			'search_in_response_to': closest_match.text,
			'exclude_text': recent_repeated_responses,
			'exclude_text_words': self.excluded_words
		}

		alternate_response_selection_parameters = {
			'search_in_response_to': self.chatbot.storage.tagger.get_bigram_pair_string(
				input_statement.text
			),
			'exclude_text': recent_repeated_responses,
			'exclude_text_words': self.excluded_words
		}

		if additional_response_selection_parameters:
			response_selection_parameters.update(additional_response_selection_parameters)
			alternate_response_selection_parameters.update(additional_response_selection_parameters)

		# Get all statements that are in response to the closest match
		response_list = list(self.chatbot.storage.filter(**response_selection_parameters))
		print('response_list',response_list)
		alternate_response_list = []

		if not response_list:
			self.chatbot.logger.info('No responses found. Generating alternate response list.')
			alternate_response_list = list(self.chatbot.storage.filter(**alternate_response_selection_parameters))

		if response_list:
			self.chatbot.logger.info(
				'Selecting response from {} optimal responses.'.format(
					len(response_list)
				)
			)
			count = len(response_list)
			
			return_response=closest_match
			largest_score=0
			MIN_SCORE = 35
			for response in response_list:
				score = self.compare_statements(response,closest_match)
				if score > largest_score and score > MIN_SCORE:
					print(response.text,'=',score)
					return_response=response
					largest_score=score
			
			print('return_response',return_response)
			print('largest_score',largest_score)
			
			if largest_score == 100.0:
				self.chatbot.read_only = False
				self.chatbot.learn_response(Statement(text=return_response.text), Statement(text=closest_match))
				self.chatbot.read_only = True		
			if return_response:
				response=return_response
			#response = response_list[random.randint(0,count-1)]
			'''response = self.select_response(
				input_statement,
				response_list,
				self.chatbot.storage
			)'''

			response.confidence = closest_match.confidence
			self.chatbot.logger.info('Response selected. Using "{}"'.format(response.text))
		elif alternate_response_list:
			print('alternate_response_list',alternate_response_list)
			'''
			The case where there was no responses returned for the selected match
			but a value exists for the statement the match is in response to.
			'''
			self.chatbot.logger.info(
				'Selecting response from {} optimal alternate responses.'.format(
					len(alternate_response_list)
				)
			)
			response = self.select_response(
				input_statement,
				alternate_response_list,
				self.chatbot.storage
			)

			response.confidence = closest_match.confidence
			self.chatbot.logger.info('Alternate response selected. Using "{}"'.format(response.text))
		else:
			print('returning default response')
			response = self.get_default_response(input_statement)

		return response
	def get(self, input_statement):
		def compare_statements(input_statement, other_statement):
			statement_text = str(input_statement.text.lower())
			other_statement_text = str(other_statement.text.lower())
			ratio=fuzz.ratio(statement_text,other_statement_text)
			partial_ratio=fuzz.ratio(statement_text,other_statement_text)
			result=((ratio*0.5)+(partial_ratio*0.5))
			
			input_parts=statement_text.split(' ')
			max_partial=result
			for part in input_parts:
				if part in other_statement_text:
					ratio=fuzz.ratio(statement_text,part)
					partial_ratio=fuzz.ratio(statement_text,part)
					result=((ratio*0.5)+(partial_ratio*0.5))
					if result > max_partial:
						max_partial = result
			self.logger.info('boosted "{}" vs "{}" = {}'.format(
				input_statement.text, other_statement.text, max_partial
			))
			return max_partial
		"""
		Takes a statement string and a list of statement strings.
		Returns the closest matching statement from the list.
		"""
		statement_list = self.chatbot.storage.get_response_statements()

		if not statement_list:
			if self.chatbot.storage.count():
				# Use a randomly picked statement
				self.logger.info(
					'No statements have known responses. ' +
					'Choosing a random response to return.'
				)
				random_response = self.chatbot.storage.get_random()
				random_response.confidence = 0
				return random_response
			else:
				raise self.EmptyDatasetException()

		closest_match = input_statement
		closest_match.confidence = 0

		# Find the closest matching known statement
		for statement in statement_list:
			confidence = compare_statements(input_statement, statement)

			if confidence > closest_match.confidence:
				statement.confidence = confidence
				closest_match = statement

		return closest_match
	
