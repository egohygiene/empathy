#!/usr/bin/env ruby
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# frozen_string_literal: true

# ==============================================================================
# 🩺 vitality.rb
# ------------------------------------------------------------------------------
# A standalone Ruby script that audits TODO comments across a repository.
#
# It enforces:
# - TODOs must include a date in the format: TODO(YYYY-MM-DD)
# - TODOs older than a configurable threshold are treated as errors
# - Undated TODOs are treated as warnings
#
# ------------------------------------------------------------------------------
# 🚀 USAGE
#
#   ruby vitality.rb [--threshold DAYS] [--path PATH]
#
# OPTIONS:
#   --threshold DAYS   Maximum allowed age of TODOs (default: 30)
#   --path PATH        Directory to scan (default: current directory)
#   --help             Show help message
#
# ------------------------------------------------------------------------------
# 🧪 EXIT CODES
#
#   0   Success (no expired TODOs)
#   1   Failure (expired TODOs found)
#   2   Invalid usage / argument error
#
# ------------------------------------------------------------------------------
# 🌱 ENVIRONMENT VARIABLES
#
#   DEBUG=1            Enable debug logging
#
# ==============================================================================

require 'date'
require 'optparse'

DEFAULT_THRESHOLD_DAYS = 30
TODO_PATTERN = /TODO(?:\((\d{4}-\d{2}-\d{2})\))?:?\s*(.*)/

options = {
  threshold: DEFAULT_THRESHOLD_DAYS,
  path: '.'
}

OptionParser.new do |parser|
  parser.banner = 'Usage: vitality.rb [options]'

  parser.on('--threshold DAYS', Integer, 'Maximum allowed TODO age') do |days|
    options[:threshold] = days
  end

  parser.on('--path PATH', String, 'Directory to scan') do |path|
    options[:path] = path
  end

  parser.on('--help', 'Show help') do
    puts parser
    exit 0
  end
end.parse!

unless options[:threshold].positive?
  warn 'threshold must be a positive number of days'
  exit 2
end

root = File.expand_path(options[:path])
unless Dir.exist?(root)
  warn "path does not exist: #{root}"
  exit 2
end

cutoff = Date.today - options[:threshold]
expired = []
undated = []

Dir.glob(File.join(root, '**', '*'), File::FNM_DOTMATCH).sort.each do |path|
  next unless File.file?(path)
  next if path.include?('/.git/')

  begin
    File.foreach(path).with_index(1) do |line, line_number|
      match = TODO_PATTERN.match(line)
      next unless match

      date_text = match[1]
      if date_text.nil?
        undated << [path, line_number, line.strip]
        next
      end

      begin
        todo_date = Date.iso8601(date_text)
      rescue Date::Error
        undated << [path, line_number, line.strip]
        next
      end

      expired << [path, line_number, line.strip, todo_date] if todo_date < cutoff
    end
  rescue ArgumentError, Encoding::InvalidByteSequenceError, Encoding::UndefinedConversionError
    next
  end
end

undated.each do |path, line_number, line|
  warn "warning: #{path}:#{line_number}: undated TODO: #{line}"
end

expired.each do |path, line_number, line, date|
  warn "error: #{path}:#{line_number}: TODO from #{date} exceeds #{options[:threshold]} days: #{line}"
end

if ENV['DEBUG'] == '1'
  warn "debug: scanned #{root}"
  warn "debug: undated TODOs=#{undated.length}"
  warn "debug: expired TODOs=#{expired.length}"
end

exit(expired.empty? ? 0 : 1)
